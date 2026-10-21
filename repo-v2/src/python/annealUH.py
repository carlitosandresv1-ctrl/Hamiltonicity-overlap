import sys, random
from familia import familia
from buscaUH import es_UH, grados_ok

def corre(n, semilla, iters):
    rng = random.Random(semilla)
    F0, H = familia(n); F = set(F0); s = len(F & H)
    mejor, arg = s, set(F)
    for t in range(iters):
        T = max(0.02, 1.0 - t / iters)      # temperatura
        Fl = sorted(F)
        i, j = rng.randrange(n), rng.randrange(n)
        if i == j: continue
        (a, b), (c, d) = Fl[i], Fl[j]
        if len({a, b, c, d}) < 4: continue
        opciones = [((a, c), (b, d)), ((a, d), (b, c))]
        rng.shuffle(opciones)
        for (x1, y1), (x2, y2) in opciones:
            e1 = (min(x1, y1), max(x1, y1)); e2 = (min(x2, y2), max(x2, y2))
            if e1 in F or e2 in F: continue
            G = set(F); G.discard(Fl[i]); G.discard(Fl[j]); G.add(e1); G.add(e2)
            if len(G) != n or not grados_ok(n, G, H): continue
            s2 = len(G & H)
            if s2 > s and rng.random() > T: continue     # a veces sube
            if es_UH(n, G, H):
                F, s = G, s2
                if s < mejor:
                    mejor, arg = s, set(F)
                    print(f"  n={n} s={s} UH  F={sorted(F)}", flush=True)
                break
    return mejor

if __name__ == "__main__":
    n = int(sys.argv[1]); iters = int(sys.argv[2])
    best = 99
    for sem in range(int(sys.argv[3])):
        best = min(best, corre(n, 1000 + sem, iters))
    print(f"n={n}: minimo s con Gamma UH tras recocido = {best}")
