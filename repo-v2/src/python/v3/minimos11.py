"""Structure of the {1,1} pairs with few good cycles (DET lines of `M=2 DETAIL=T near111`).

For each pair: dihedral class (symmetries of H that keep the two stretches), the cycles of F,
and for each cycle whether its vertex set is an interval of consecutive vertices of H.
Prints one line per class: n, g (good cycles), p (position of the second stretch), the
F-cycle profile, and a canonical F.
usage: python3 minimos11.py det_files...
"""
import re
import sys
from collections import Counter, defaultdict


def E(a, b):
    return (min(a, b), max(a, b))


def images(n, p, F):
    """the images of (p, F) under the dihedral maps that send the stretches to {01, p'(p'+1)}"""
    maps = [lambda x: x, lambda x: (p + 1 - x) % n,          # keep {01} at 01
            lambda x: (x - p) % n, lambda x: (1 - x) % n]     # swap the two stretches
    out = []
    for f in maps:
        G = sorted(E(f(a), f(b)) for a, b in F)
        S = [e for e in G if (e[1] - e[0]) % n in (1, n - 1)]
        assert (0, 1) in S, (n, p, G)
        q = [e for e in S if e != (0, 1)][0][0]
        out.append((q, tuple(G)))
    return out


def fcycles(n, F):
    adj = defaultdict(list)
    for a, b in F:
        adj[a].append(b); adj[b].append(a)
    seen, cyc = set(), []
    for s in range(n):
        if s in seen:
            continue
        c, prev, v = [s], None, s
        seen.add(s)
        while True:
            w = adj[v][0] if adj[v][0] != prev else adj[v][1]
            if w == s:
                break
            c.append(w); seen.add(w); prev, v = v, w
        cyc.append(c)
    return cyc


def interval(n, vs):
    """True when the vertex set vs is a set of consecutive vertices of H (cyclically)"""
    s = set(vs)
    if len(s) == n:
        return True
    starts = [v for v in s if (v - 1) % n not in s]
    return len(starts) == 1


def profile(n, F):
    parts = []
    for c in fcycles(n, F):
        parts.append('%d%s' % (len(c), 'i' if interval(n, c) else ''))
    return '+'.join(sorted(parts, key=lambda t: (-int(t.rstrip('i')), t)))


classes = {}
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith('DET'):
            continue
        n = int(re.search(r'n=(\d+)', line).group(1))
        p = int(re.search(r'p=0,(\d+)', line).group(1))
        g = int(re.search(r'good=(\d+)', line).group(1))
        F = [tuple(map(int, t.split('-'))) for t in line.split('F=')[1].split()]
        key = min(images(n, p, F))
        classes.setdefault((n, g, key), 0)
        classes[(n, g, key)] += 1

summary = Counter()
for (n, g, (q, G)), mult in sorted(classes.items()):
    prof = profile(n, G)
    summary[(n, g, prof)] += 1
    print('CLASS n=%d g=%d p=%d labelled=%d Fcycles=%s F=%s' % (
        n, g, q, mult, prof, ' '.join('%d-%d' % e for e in G)))
for (n, g, prof), c in sorted(summary.items()):
    print('PROFILE n=%d g=%d Fcycles=%s classes=%d' % (n, g, prof, c))
