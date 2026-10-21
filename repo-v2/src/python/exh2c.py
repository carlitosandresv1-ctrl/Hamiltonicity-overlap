"""Busqueda EXHAUSTIVA del maximo de cor(F) sobre 2-factores con c ciclos.

Reduccion: si G es hamiltoniano y F es un 2-factor de G, sea H un ciclo
hamiltoniano de G.  Entonces G' = F u H es hamiltoniano, contiene F, y
cor_{G'}(F) >= cor_G(F) (menos ciclos hamiltonianos disponibles).  Luego el
supremo de cor sobre todos los pares (G,F) con c(F)=c se alcanza en grafos de
la forma  G = F u H  con H hamiltoniano.

Asi que: fijamos H = (0,1,...,n-1) y recorremos TODOS los 2-factores F con
exactamente c ciclos sobre [n].  Simetria: el estabilizador de H es el grupo
diedral de orden 2n, que actua sobre los F; lo usamos como filtro canonico.
"""
import sys
from itertools import combinations, permutations
from cor2 import cor


def ciclos_de(vs):
    """todos los ordenes ciclicos de la lista vs, sin repetir por rotacion ni
    por reflexion; devuelve el conjunto de aristas."""
    vs = list(vs)
    if len(vs) < 3:
        return
    a = vs[0]
    resto = vs[1:]
    vistos = set()
    for p in permutations(resto):
        if p[0] > p[-1]:
            continue                      # quita reflexiones
        cic = (a,) + p
        ar = frozenset(
            (min(cic[i], cic[(i + 1) % len(cic)]), max(cic[i], cic[(i + 1) % len(cic)]))
            for i in range(len(cic))
        )
        if ar in vistos:
            continue
        vistos.add(ar)
        yield ar


def dos_factores(n, c):
    """2-factores con exactamente c ciclos, c = 2 o 3."""
    V = list(range(n))
    if c == 2:
        for k in range(3, n // 2 + 1):
            for A in combinations(V, k):
                if 0 not in A:
                    continue
                B = [v for v in V if v not in A]
                if len(B) < 3:
                    continue
                if len(B) == k and A[1] > B[0]:
                    continue              # parte no canonica (desempate)
                for ca in ciclos_de(A):
                    for cb in ciclos_de(B):
                        yield ca | cb
    elif c == 3:
        for k1 in range(3, n + 1):
            for A in combinations(V, k1):
                if 0 not in A:
                    continue
                R = [v for v in V if v not in A]
                if len(R) < 6:
                    continue
                for k2 in range(3, len(R) - 2):
                    for Bc in combinations(R, k2):
                        if R[0] not in Bc:
                            continue
                        C = [v for v in R if v not in Bc]
                        if len(C) < 3:
                            continue
                        if len(Bc) == len(C) and Bc[1] > C[0]:
                            continue
                        if len(A) == len(Bc) and A[0] > Bc[0]:
                            continue
                        for ca in ciclos_de(A):
                            for cb in ciclos_de(Bc):
                                for cc in ciclos_de(C):
                                    yield ca | cb | cc


def canon_diedral(n, F):
    """clave canonica de F bajo el diedral que preserva el ciclo canonico H"""
    mejor = None
    for s in range(n):
        for d in (1, -1):
            img = frozenset(
                (min((u * d + s) % n, (v * d + s) % n),
                 max((u * d + s) % n, (v * d + s) % n))
                for (u, v) in F
            )
            k = tuple(sorted(img))
            if mejor is None or k < mejor:
                mejor = k
    return mejor


def main(n, c, tope):
    H = set((min(i, (i + 1) % n), max(i, (i + 1) % n)) for i in range(n))
    vistos = set()
    mejor, arg = -1, None
    tot = 0
    for F in dos_factores(n, c):
        k = canon_diedral(n, F)
        if k in vistos:
            continue
        vistos.add(k)
        tot += 1
        E = set(F) | H
        v = cor(n, set(F), E, tope=tope)
        if v > mejor:
            mejor, arg = v, sorted(F)
            print("  nuevo max cor =", v, " F =", arg, flush=True)
    print(f"n={n} c={c}: {tot} clases de 2-factores, max cor = {mejor}")
    print("  extremal:", arg)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 6)
