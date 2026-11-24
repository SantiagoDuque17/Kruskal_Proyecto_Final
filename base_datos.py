"""
Conexión y operaciones de persistencia en MySQL.
Requiere: pip install mysql-connector-python
"""

import mysql.connector

from grafo import Grafo, Localidad, Tramo
from kruskal import ResultadoKruskal


class BaseDatos:
    def __init__(
        self,
        host: str = "127.0.0.1",
        puerto: int = 3306,
        usuario: str = "root",
        clave: str = "",
        base_datos: str = "fibra_optica"
    ) -> None:
        self.conexion = mysql.connector.connect(
            host=host,
            port=puerto,
            user=usuario,
            password=clave,
            database=base_datos
        )

    def obtener_grafo(self) -> Grafo:
        cursor = self.conexion.cursor()

        cursor.execute(
            "SELECT codigo, nombre FROM localidades ORDER BY FIELD(codigo, 'U', 'C', 'T', 'S', 'K', 'F', 'B')"
        )
        localidades = [
            Localidad(codigo, nombre)
            for codigo, nombre in cursor.fetchall()
        ]

        cursor.execute(
            "SELECT origen, destino, costo FROM tramos ORDER BY costo, id"
        )
        tramos = [
            Tramo(origen, destino, int(costo))
            for origen, destino, costo in cursor.fetchall()
        ]

        cursor.close()
        return Grafo(localidades, tramos)

    def guardar_resultado(self, resultado: ResultadoKruskal) -> int:
        cursor = self.conexion.cursor()

        try:
            cursor.execute(
                "INSERT INTO ejecuciones (algoritmo, costo_total) VALUES (%s, %s)",
                (resultado.algoritmo, resultado.costo_total)
            )
            ejecucionId = cursor.lastrowid

            cursor.executemany(
                """
                INSERT INTO pasos_ejecucion
                (ejecucion_id, orden, origen, destino, costo, aceptado, motivo, conjuntos)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    (
                        ejecucionId,
                        paso.orden,
                        paso.tramo.origen,
                        paso.tramo.destino,
                        paso.tramo.costo,
                        paso.aceptado,
                        paso.motivo,
                        paso.conjuntos
                    )
                    for paso in resultado.pasos
                ]
            )

            self.conexion.commit()
            return ejecucionId

        except Exception:
            self.conexion.rollback()
            raise

        finally:
            cursor.close()

    def cerrar(self) -> None:
        self.conexion.close()