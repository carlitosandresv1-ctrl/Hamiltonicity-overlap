"""Busqueda dirigida de uniones UNIVOCAMENTE HAMILTONIANAS con s pequeno.

Si existe Gamma = F u H univocamente Hamiltoniano con s = |F cap H| <= 4,
entonces ov(n) = s <= 4 y la conjetura ov(n) = 5 es FALSA.

Estado: el 2-factor F (H es el ciclo canonico).  Movimiento: 2-opt sobre F.
Restriccion: Gamma debe ser univocamente Hamiltoniano.  Objetivo: minimizar s.
Arranque: la familia Gamma_n, que es UH con s = 5.
"""
import sys, random
from familia import familia


def nham(n, ady, tope=2):
    """cuenta ciclos Hamiltonianos (parando en tope), por retroceso"""
    total = 0
    vis = [False] * n
    vis[0] = True
    cam = [0]

    def dfs(v):
        nonlocal total
        if total >= tope:
            return
        if len(cam) == n:
            if 0 in ady[v]:
                total += 1
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
    return total // 2


def adyacencia(n, E):
    ady = [[] for _ in range(n)]
    for (u, v) in E:
        ady[u].append(v)
        ady[v].append(u)
    return ady


def es_UH(n, F, H):
    return nham(n, adyacencia(n, F | H), tope=4) == 1


def grados_ok(n, F, H):
    """2-factor valido: 2-regular y simple"""
    g = [0] * n
    for (u, v) in F:
        g[u] += 1
        g[v] += 1
    return all(x == 2 for x in g)


def main(n, semilla, iters):
    rng = random.Random(semilla)
    F0, H = familia(n)
    F = set(F0)
    assert es_UH(n, F, H), "el arranque deberia ser UH"
    s = len(F & H)
    mejor = s
    mejorF = set(F)
    for t in range(iters):
        Fl = sorted(F)
        i, j = rng.randrange(n), rng.randrange(n)
        if i == j:
            continue
        (a, b), (c, d) = Fl[i], Fl[j]
        if len({a, b, c, d}) < 4:
            continue
        for (x1, y1), (x2, y2) in (((a, c), (b, d)), ((a, d), (b, c))):
            e1 = (min(x1, y1), max(x1, y1))
            e2 = (min(x2, y2), max(x2, y2))
            if e1 in F or e2 in F:
                continue
            G = set(F)
            G.discard(Fl[i]); G.discard(Fl[j])
            G.add(e1); G.add(e2)
            if len(G) != n or not grados_ok(n, G, H):
                continue
            s2 = len(G & H)
            if s2 <= s and es_UH(n, G, H):
                F, s = G, s2
                if s < mejor:
                    mejor = s
                    mejorF = set(F)
                    print(f"  n={n}  s={s}  UH!  F = {sorted(F)}", flush=True)
                break
    print(f"n={n}: minimo s alcanzado con Gamma UH = {mejor}")
    return mejor, mejorF


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
