"""Comprueba la proposicion de supresion sobre todas las clases UH halladas.

Supresion: en Gamma = F u H se suprimen los vertices de grado 2, es decir cada
tramo de S se sustituye por una sola arista (MARCADA) entre sus extremos.  El
resultado Gamma^flat es un multigrafo.

Lo que hay que comprobar:
  (a) #Ham(Gamma) = #Ham(Gamma^flat que pasan por las c aristas marcadas)
  (b) si Gamma^flat es o no univocamente Hamiltoniano a secas
"""
import re, sys
from collections import Counter


def tramos(S):
    ady = {}
    for (a, b) in S:
        ady.setdefault(a, []).append(b)
        ady.setdefault(b, []).append(a)
    vis, out = set(), []
    for v in ady:
        if v in vis or len(ady[v]) != 1:
            continue                      # arrancar por un extremo
        cam = [v]; vis.add(v); w = ady[v][0]
        while True:
            cam.append(w); vis.add(w)
            sig = [x for x in ady[w] if x != cam[-2]]
            if not sig: break
            w = sig[0]
        out.append(cam)
    return out


def nham(n, E, obligadas=()):
    """cuenta ciclos hamiltonianos; E es lista de aristas (multigrafo: repetidas
    con etiqueta). Cada arista es (u,v,id). 'obligadas' = ids que deben usarse."""
    ady = {v: [] for v in range(n)}
    for (u, v, i) in E:
        ady[u].append((v, i)); ady[v].append((u, i))
    obl = set(obligadas)
    tot = 0
    vis = [False] * n; vis[0] = True
    cam = [0]; usadas = []

    def dfs(v):
        nonlocal tot
        if len(cam) == n:
            for (w, i) in ady[v]:
                if w == 0 and cam[1] < cam[-1]:
                    if obl <= set(usadas + [i]):
                        tot += 1
            return
        for (w, i) in ady[v]:
            if vis[w]: continue
            vis[w] = True; cam.append(w); usadas.append(i)
            dfs(w)
            usadas.pop(); cam.pop(); vis[w] = False
    dfs(0)
    return tot


def analiza(n, F):
    H = {tuple(sorted((i, (i + 1) % n))) for i in range(n)}
    F = {tuple(sorted(e)) for e in F}
    G = F | H
    S = F & H
    T = tramos(S)
    c = len(T)
    interiores = {v for cam in T for v in cam[1:-1]}
    sobrevive = [v for v in range(n) if v not in interiores]
    ren = {v: i for i, v in enumerate(sobrevive)}
    E = []
    k = 0
    for (u, v) in G:
        if u in interiores or v in interiores: continue
        E.append((ren[u], ren[v], k)); k += 1
    marcadas = []
    for cam in T:
        if len(cam) == 2:
            # tramo de una sola arista: ya esta en E, solo hay que marcarla
            a, b = ren[cam[0]], ren[cam[1]]
            for (u, v, i) in E:
                if {u, v} == {a, b}: marcadas.append(i); break
        else:
            E.append((ren[cam[0]], ren[cam[-1]], k)); marcadas.append(k); k += 1
    m = len(sobrevive)
    g = Counter()
    for (u, v, _) in E: g[u] += 1; g[v] += 1
    return dict(n=n, c=c, m=m, perfil=dict(sorted(Counter(g.values()).items())),
                ham_gamma=nham(n, [(u, v, i) for i, (u, v) in enumerate(G)]),
                ham_flat=nham(m, E),
                ham_flat_marcadas=nham(m, E, marcadas),
                paralelas=sum(1 for i in marcadas
                              for (u, v, j) in E
                              if j != i and {u, v} == {E[i][0], E[i][1]}))


if __name__ == "__main__":
    malo = 0; total = 0
    for n in (10, 11, 12, 13):
        for ln in open(f'cl5_{n}.txt'):
            if not ln.startswith('  clase'): continue
            pares = re.findall(r'\((\d+),(\d+)\)', ln.split('S =')[0])
            F = [(int(a), int(b)) for a, b in pares]
            r = analiza(n, F)
            total += 1
            ok = (r['ham_gamma'] == 1 and r['ham_flat_marcadas'] == 1)
            if not ok: malo += 1
            print(f"n={r['n']} c={r['c']} m={r['m']} perfil={r['perfil']} "
                  f"ham(G)={r['ham_gamma']} ham(G^b)={r['ham_flat']} "
                  f"ham(G^b|marcadas)={r['ham_flat_marcadas']} paralelas={r['paralelas']}"
                  + ("" if ok else "   <<< FALLA"))
    print(f"--- {total} clases, {malo} fallos de la correspondencia")
