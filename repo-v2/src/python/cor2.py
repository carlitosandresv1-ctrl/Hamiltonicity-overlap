"""Test exacto de cor(F) por ensamblaje de caminos.

cor(F) = min_{H ham} |F menos H|.  Si |F menos H| = j, entonces H contiene F menos j
aristas, es decir contiene el bosque lineal F-R con |R|=j, y lo cierra con j
aristas de G.  Luego:

   cor(F) = min { j : existe R subconjunto de F, |R|=j, tal que los caminos de
                  F-R admiten un orden ciclico y orientaciones con extremos
                  consecutivos unidos por aristas de G }

Buscamos j = c, c+1, ... hasta tope.  Coste: C(n,j) * (j-1)! * 2^(j-1).
"""
from itertools import combinations, permutations, product


def caminos(n, F, R):
    """Devuelve lista de caminos (como listas de vertices) de F-R, o None si
    F-R no es un bosque lineal cubriendo todos los vertices."""
    ady = [[] for _ in range(n)]
    for (u, v) in F:
        if (u, v) in R:
            continue
        ady[u].append(v)
        ady[v].append(u)
    # cada vertice grado <=2; cualquier ciclo restante -> None
    vis = [False] * n
    out = []
    for s in range(n):
        if vis[s] or len(ady[s]) == 2:
            continue
        # extremo de camino (grado 0 o 1)
        vis[s] = True
        cam = [s]
        prev, cur = None, s
        while True:
            sig = [w for w in ady[cur] if w != prev]
            if not sig:
                break
            prev, cur = cur, sig[0]
            vis[cur] = True
            cam.append(cur)
        out.append(cam)
    if not all(vis):
        return None          # queda un ciclo
    return out


def ensamblable(caminos_, Eset):
    """Existe orden ciclico + orientacion de los caminos con extremos
    consecutivos adyacentes en G?"""
    k = len(caminos_)
    if k == 1:
        c = caminos_[0]
        return (min(c[0], c[-1]), max(c[0], c[-1])) in Eset
    # fijamos el camino 0 con orientacion fija (simetria dihedral)
    base = caminos_[0]
    resto = caminos_[1:]
    for perm in permutations(range(k - 1)):
        for ori in product((0, 1), repeat=k - 1):
            seq = [base]
            for idx, o in zip(perm, ori):
                c = resto[idx]
                seq.append(c[::-1] if o else c)
            ok = True
            for i in range(k):
                a = seq[i][-1]
                b = seq[(i + 1) % k][0]
                if (min(a, b), max(a, b)) not in Eset:
                    ok = False
                    break
            if ok:
                return True
    return False


def cor(n, F, Eset, tope=6):
    """cor(F) exacto si <= tope; devuelve tope+1 si excede."""
    Fl = sorted(F)
    # j = 0 : F ya es hamiltoniano
    ady = [[] for _ in range(n)]
    for (u, v) in F:
        ady[u].append(v)
        ady[v].append(u)
    vis, cur, prev, cnt = [False] * n, 0, None, 0
    while not vis[cur]:
        vis[cur] = True
        cnt += 1
        sig = [w for w in ady[cur] if w != prev]
        prev, cur = cur, sig[0]
    if cnt == n:
        return 0
    for j in range(1, tope + 1):
        for R in combinations(Fl, j):
            cs = caminos(n, F, set(R))
            if cs is None or len(cs) != j:
                continue
            if ensamblable(cs, Eset):
                return j
    return tope + 1
