"""Propagacion de forzado en G = F u H.

Reglas (validas para cualquier ciclo hamiltoniano H' de G):
 (R1) si en v quedan exactamente 2 aristas no excluidas, ambas estan en H';
 (R2) si en v hay 2 aristas forzadas, las demas incidentes quedan excluidas;
 (R3) si u y v son extremos de un mismo camino forzado con menos de n aristas,
      la arista uv queda excluida (cerraria un ciclo corto).

Si la propagacion fuerza las n aristas de H, entonces G es unicamente
hamiltoniano y cor(F) = |F \\ H| = n - |F cap H|.
"""
import sys
from familia import familia


def propaga(n, E, traza=False):
    E = sorted(E)
    forz, excl = set(), set()
    padre = list(range(n))        # union-find sobre aristas forzadas
    gradof = [0] * n

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    ady = {v: set() for v in range(n)}
    for (u, v) in E:
        ady[u].add(v)
        ady[v].add(u)

    pasos = []
    cambio = True
    while cambio:
        cambio = False
        # R1
        for v in range(n):
            if gradof[v] == 2:
                continue
            libres = [w for w in ady[v]
                      if (min(v, w), max(v, w)) not in excl
                      and (min(v, w), max(v, w)) not in forz]
            if len(libres) + gradof[v] == 2 and libres:
                for w in libres:
                    e = (min(v, w), max(v, w))
                    forz.add(e)
                    gradof[e[0]] += 1
                    gradof[e[1]] += 1
                    padre[raiz(e[0])] = raiz(e[1])
                    pasos.append(('forzada', e, f'grado libre en {v}'))
                cambio = True
        # R2
        for v in range(n):
            if gradof[v] < 2:
                continue
            for w in list(ady[v]):
                e = (min(v, w), max(v, w))
                if e not in forz and e not in excl:
                    excl.add(e)
                    pasos.append(('excluida', e, f'{v} saturado'))
                    cambio = True
        # R3
        for (u, v) in E:
            e = (u, v)
            if e in forz or e in excl:
                continue
            if raiz(u) == raiz(v) and len(forz) < n - 1:
                excl.add(e)
                pasos.append(('excluida', e, 'cerraria ciclo corto'))
                cambio = True
    if traza:
        for t in pasos:
            print('   ', t)
    return forz, excl


if __name__ == "__main__":
    hasta = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    print(" n    aristas forzadas    = H ?")
    for n in range(10, hasta + 1):
        F, H = familia(n)
        forz, excl = propaga(n, F | H)
        print(f"{n:3d} {len(forz):17d}    {'SI' if forz == H else 'NO  ' + str(sorted(H ^ forz))}")
