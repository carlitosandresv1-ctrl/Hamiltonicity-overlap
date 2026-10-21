"""True number of good cycles of each C3FAIL pair (the CAP of near111 truncates good=);
checks that every good cycle keeps S, whether H* is present, and lists pairs with an even count.
usage: python3 c3_buenos.py results/v3/claims3_11_n8_12.txt"""
import sys, re
from collections import Counter
def E(a, b): return (min(a, b), max(a, b))
out = Counter(); hstar = Counter()
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith('C3FAIL'): continue
        n = int(re.search(r'n=(\d+)', line).group(1))
        F = {E(*map(int, t.split('-'))) for t in line.split('F=')[1].split()}
        H = {E(i, (i + 1) % n) for i in range(n)}; S = F & H; U = H - S
        adj = {v: set() for v in range(n)}
        for a, b in F | H: adj[a].add(b); adj[b].add(a)
        cyc = []; path = [0]; seen = {0}
        def rec():
            v = path[-1]
            if len(path) == n:
                if 0 in adj[v] and path[1] < path[-1]: cyc.append({E(path[i], path[(i + 1) % n]) for i in range(n)})
                return
            for w in adj[v]:
                if w not in seen: seen.add(w); path.append(w); rec(); path.pop(); seen.discard(w)
        rec()
        good = [C for C in cyc if not U <= C]
        assert all(S <= C for C in good)          # C3 fails: every good cycle keeps S
        nS = sum(S <= C for C in cyc); hs = any(U <= C and not S <= C for C in cyc)
        out[(n, len(good))] += 1; hstar[(n, hs)] += 1
        if len(good) % 2 == 0: print('EVEN', n, len(good), 'S=', sorted(S), line.split('F=')[1].strip())
for n in sorted({k[0] for k in out}):
    ev = sum(c for (m, g), c in out.items() if m == n and g % 2 == 0)
    print('n=%d even:%d odd:%d' % (n, ev, sum(c for (m, g), c in out.items() if m == n) - ev))
    print('n=%d true good among C3FAIL:' % n, sorted((g, c) for (m, g), c in out.items() if m == n), '| H* present:', hstar[(n, True)], 'absent:', hstar[(n, False)])
