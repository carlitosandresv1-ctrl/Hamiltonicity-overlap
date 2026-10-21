"""Verificacion exhaustiva del lema de aristas protegidas.

LEMA.  Si H es optimo en Gamma = F u H (es decir, ov_Gamma(F) = |F cap H|),
entonces todo ciclo Hamiltoniano H' de Gamma cumple  H \\ H'  contenido en F cap H:
un ciclo rival solo puede renunciar a aristas compartidas.
"""
import sys
from itertools import combinations, permutations


def todos_2factores(n):
    """genera todos los 2-factores de [n] como frozensets de aristas"""
    def rec(libres, aristas):
        if not libres:
            yield frozenset(aristas)
            return
        v = libres[0]
        resto = libres[1:]
        for k in range(2, len(resto) + 1):
            for S in combinations(resto, k):
                sig = [w for w in resto if w not in S]
                for p in permutations(S):
                    if p[0] > p[-1]:
                        continue          # mata reflexiones
                    cic = (v,) + p
                    nuevas = []
                    for i in range(len(cic)):
                        x, y = cic[i], cic[(i + 1) % len(cic)]
                        nuevas.append((min(x, y), max(x, y)))
                    yield from rec(sig, aristas + nuevas)
    yield from rec(list(range(n)), [])


def ciclos_ham(n, E):
    ady = [[] for _ in range(n)]
    for (u, v) in E:
        ady[u].append(v)
        ady[v].append(u)
    out = []
    cam = [0]
    vis = [False] * n
    vis[0] = True

    def dfs(v):
        if len(cam) == n:
            if 0 in ady[v]:
                ar = frozenset((min(cam[i], cam[(i + 1) % n]),
                                max(cam[i], cam[(i + 1) % n])) for i in range(n))
                out.append(ar)
            return
        for w in ady[v]:
            if vis[w]:
                continue
            vis[w] = True
            cam.append(w)
            dfs(w)
            cam.pop()
            vis[w] = False
    dfs(0)
    return set(out)


def main(n):
    H = frozenset((min(i, (i + 1) % n), max(i, (i + 1) % n)) for i in range(n))
    opt = 0
    mal = 0
    maxham = 0
    tot = 0
    for F in todos_2factores(n):
        tot += 1
        hs = ciclos_ham(n, F | H)
        if not hs:
            continue
        ov = max(len(F & T) for T in hs)
        S = F & H
        if len(S) != ov:
            continue                      # H no es optimo
        opt += 1
        maxham = max(maxham, len(hs))
        for T in hs:
            if not (H - T) <= S:
                mal += 1
                print("  VIOLACION", sorted(F), " H-H' =", sorted(H - T),
                      " S =", sorted(S))
                break
    print(f"n={n}: {tot} 2-factores, {opt} con H optimo, violaciones = {mal}, "
          f"max #ciclos ham = {maxham}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 9)
