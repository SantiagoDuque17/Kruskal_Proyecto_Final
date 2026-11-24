"""
Estructuras del problema: localidades, tramos y grafo.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Localidad:
    codigo: str
    nombre: str


@dataclass(frozen=True)
class Tramo:
    origen: str
    destino: str
    costo: int  # millones de pesos

    def __str__(self) -> str:
        return f"{self.origen}-{self.destino}"


class Grafo:
    def __init__(self, localidades: list[Localidad], tramos: list[Tramo]) -> None:
        self.localidades = localidades
        self.tramos = tramos

    def obtener_localidades(self) -> list[Localidad]:
        return list(self.localidades)

    def obtener_tramos(self) -> list[Tramo]:
        return list(self.tramos)