"""
Punto de entrada del proyecto.
Ejecuta Kruskal usando los datos almacenados en MySQL.
"""

from base_datos import BaseDatos
from kruskal import Kruskal


def mostrar_resultado(resultado) -> None:
    print(f"\n=== {resultado.algoritmo} ===")
    print(
        f"{'Paso':<5}{'Arista':<8}{'Costo':<7}"
        f"{'Decision':<11}{'Motivo':<38}Conjuntos"
    )
    print("-" * 110)

    for paso in resultado.pasos:
        decision = "ACEPTA" if paso.aceptado else "RECHAZA"
        print(
            f"{paso.orden:<5}{str(paso.tramo):<8}{paso.tramo.costo:<7}"
            f"{decision:<11}{paso.motivo:<38}{paso.conjuntos}"
        )

    print("\nArbol de costo minimo:")
    for tramo in resultado.arbol:
        print(f"  {tramo}  ({tramo.costo})")

    print(f"\nCosto total minimo: {resultado.costo_total} millones de pesos")


def main() -> None:
    baseDatos = None

    try:
        baseDatos = BaseDatos(
            host="127.0.0.1",
            puerto=3306,
            usuario="root",
            clave="",
            base_datos="fibra_optica"
        )

        grafo = baseDatos.obtener_grafo()
        algoritmo = Kruskal()
        resultado = algoritmo.resolver(grafo)

        mostrar_resultado(resultado)

        ejecucionId = baseDatos.guardar_resultado(resultado)
        print(f"\nResultado guardado en MySQL (ejecuciones.id = {ejecucionId})")

    except Exception as error:
        print(f"Error al ejecutar el proyecto: {error}")

    finally:
        if baseDatos is not None:
            baseDatos.cerrar()


if __name__ == "__main__":
    main()
