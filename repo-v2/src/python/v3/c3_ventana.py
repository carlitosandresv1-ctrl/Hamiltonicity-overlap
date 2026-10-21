"""For each C3FAIL pair: least L such that some window W = {i, ..., i+L-1} of consecutive
vertices has a Hamilton path of Gamma[W + {i-1, i+L}] from i-1 to i+L, other than the H-path,
that gives up an unshared H-edge.  Such a path, completed by the rest of H, is a good cycle."""
import sys, re
from collections import Counter
def E(a, b): return (min(a, b), max(a, b))
res = Counter(); good = Counter(); worst = {}
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith('C3FAIL'): continue
        n = int(re.search(r'n=(\d+)', line).group(1)); g = int(re.search(r'good=(\d+)', line).group(1))
        F = {E(*map(int, t.split('-'))) for t in line.split('F=')[1].split()}
        H = {E(i, (i + 1) % n) for i in range(n)}
        U = H - F; G = F | H
        adj = {v: set() for v in range(n)}
        for a, b in G: adj[a].add(b); adj[b].add(a)
        best = None
        for L in range(2, n - 1):
            for i in range(n):
                W = [(i + t) % n for t in range(L)]; s, t = (i - 1) % n, (i + L) % n
                allowed = set(W) | {s, t}
                need = {E(W[k], W[k + 1]) for k in range(L - 1)} | {E(s, W[0]), E(W[-1], t)}
                needU = need & U
                box = [False]; path = [s]; seen = {s}
                def rec():
                    if box[0]: return
                    v = path[-1]
                    if len(path) == L + 2:
                        if v == t:
                            es = {E(path[k], path[k + 1]) for k in range(L + 1)}
                            if not needU <= es: box[0] = True
                        return
                    for w in adj[v]:
                        if w in allowed and w not in seen and (w != t or len(path) == L + 1):
                            seen.add(w); path.append(w); rec(); path.pop(); seen.discard(w)
                rec()
                if box[0]: best = L; break
            if best: break
        res[(n, best)] += 1; good[(n, g)] += 1
        if best and best >= worst.get(n, (0,))[0]: worst[n] = (best, line.strip())
for k in sorted(res, key=lambda x: (x[0], x[1] or 99)): print('n=%d least window L=%s : %d' % (k[0], k[1], res[k]))
print('good among C3FAIL:', sorted(good.items()))
for n, (L, l) in sorted(worst.items()): print('widest n=%d L=%d %s' % (n, L, l))
