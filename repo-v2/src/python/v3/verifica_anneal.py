"""Independent recount of the good cycles of BEST lines with good <= LIMIT."""
import sys, re
sys.setrecursionlimit(10000)
LIMIT = 15
def E(a, b): return (min(a, b), max(a, b))
ok = bad = 0
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith('BEST'): continue
        g0 = int(re.search(r'good=(\d+)', line).group(1))
        if g0 > LIMIT: continue
        n = int(re.search(r'n=(\d+)', line).group(1))
        F = {E(*map(int, t.split('-'))) for t in line.split('F=')[1].split()}
        H = {E(i, (i + 1) % n) for i in range(n)}; S = F & H; U = H - S
        assert len(S) == 2 and all(sum(v in e for e in F) == 2 for v in range(n))
        adj = {v: set() for v in range(n)}
        for a, b in F | H: adj[a].add(b); adj[b].add(a)
        cyc = []; path = [0]; seen = {0}
        def rec():
            v = path[-1]
            if len(path) == n:
                if 0 in adj[v] and path[1] < path[-1]:
                    cyc.append({E(path[i], path[(i + 1) % n]) for i in range(n)})
                return
            for w in adj[v]:
                if w not in seen: seen.add(w); path.append(w); rec(); path.pop(); seen.discard(w)
        rec()
        good = [C for C in cyc if not U <= C]
        c3fail = all(S <= C for C in good)
        cls = 'C3FAIL' if c3fail and good else ('RIGID' if not good else 'other')
        match = len(good) == g0 and cls in line
        ok += match; bad += not match
        print(fn.split('/')[-1], 'n=%d' % n, 'C=%d good=%d (C says %d) class=%s total_HC=%d %s' %
              (n, len(good), g0, cls, len(cyc), 'OK' if match else 'MISMATCH'))
print('verified', ok, 'mismatches', bad)
