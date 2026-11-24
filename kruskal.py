"""
Implementación del algoritmo de Kruskal con estructura Union-Find.
"""

from dataclasses import dataclass
from grafo import Grafo, Tramo


@dataclass
class PasoKruskal:
    orden: int
    tramo: Tramo
    aceptado: bool
    motivo: str
    conjuntos: str


@dataclass
class ResultadoKruskal:
    algoritmo: str
    pasos: list[PasoKruskal]
    arbol: list[Tramo]
    costo_total: int


class UnionFind:
    def __init__(self, elementos: list[str]) -> None:
        self._orden = list(elementos)
        self._padre = {elemento: elemento for elemento in elementos}
        self._rango = {elemento: 0 for elemento in elementos}

    def find(self, elemento: str) -> str:
        if self._padre[elemento] != elemento:
            self._padre[elemento] = self.find(self._padre[elemento])
        return self._padre[elemento]

    def union(self, primero: str, segundo: str) -> bool:
        raizPrimero = self.find(primero)
        raizSegundo = self.find(segundo)

        if raizPrimero == raizSegundo:
            return False

        if self._rango[raizPrimero] < self._rango[raizSegundo]:
            self._padre[raizPrimero] = raizSegundo
        elif self._rango[raizPrimero] > self._rango[raizSegundo]:
            self._padre[raizSegundo] = raizPrimero
        else:
            self._padre[raizSegundo] = raizPrimero
            self._rango[raizPrimero] += 1

        return True

    def conjuntos(self) -> str:
        grupos: dict[str, list[str]] = {}

        for elemento in self._orden:
            raiz = self.find(elemento)
            grupos.setdefault(raiz, []).append(elemento)

        return " ".join("{" + ",".join(grupo) + "}" for grupo in grupos.values())


class Kruskal:
    def resolver(self, grafo: Grafo) -> ResultadoKruskal:
        codigos = [localidad.codigo for localidad in grafo.obtener_localidades()]
        unionFind = UnionFind(codigos)

        tramosOrdenados = sorted(
            grafo.obtener_tramos(),
            key=lambda tramo: tramo.costo
        )

        pasos = []
        arbol = []
        costoTotal = 0

        for indice, tramo in enumerate(tramosOrdenados, start=1):
            if unionFind.find(tramo.origen) == unionFind.find(tramo.destino):
                aceptado = False
                motivo = "mismo conjunto: formaría un ciclo"
            elif len(arbol) == len(codigos) - 1:
                aceptado = False
                motivo = "árbol completo (n-1 aristas)"
            else:
                unionFind.union(tramo.origen, tramo.destino)
                arbol.append(tramo)
                costoTotal += tramo.costo
                aceptado = True
                motivo = "conjuntos distintos, no hay ciclo"

            pasos.append(
                PasoKruskal(
                    indice,
                    tramo,
                    aceptado,
                    motivo,
                    unionFind.conjuntos()
                )
            )

        return ResultadoKruskal("Kruskal", pasos, arbol, costoTotal)
