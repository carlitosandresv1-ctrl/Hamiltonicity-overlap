"""Independent check of near11 / near111 for small n.

Enumerates ALL 2-factors of K_n from scratch (no shared code with the C programs), keeps
those whose intersection with H = (0,1,...,n-1) is M pairwise disjoint single edges, one of
them 01, enumerates ALL Hamilton cycles of F u H, and reports the same quantities as the C
programs: number of pairs, histogram of good cycles (good = gives up an unshared H-edge),
rigid pairs (no good cycle, Cor. 7.9) and the least number t of chords in a good cycle.

usage: python3 verifica_unit.py n M
"""
import sys
from collections import Counter
from itertools import combinations


def two_factors(n):
    """All 2-factors of K_n as frozensets of edges (a, b), a < b."""
    out = []

    def cycles_from(rest, acc):
        if not rest:
            out.append(frozenset(acc))
            return
        v = min(rest)
        others = sorted(rest - {v})
        for k in range(2, len(others) + 1):
            for comb in combinations(others, k):
                if len(rest) - 1 - k in (1, 2):      # leftover too small for a cycle
                    continue
                # cycles through v on {v} + comb, each counted once (fix direction)
                for perm in perms(list(comb)):
                    if perm[0] > perm[-1]:
                        continue
                    cyc = [v] + list(perm)
                    edges = [tuple(sorted((cyc[i], cyc[(i + 1) % len(cyc)]))) for i in range(len(cyc))]
                    cycles_from(rest - {v} - set(comb), acc + edges)

    def perms(xs):
        if len(xs) <= 1:
            yield list(xs)
            return
        for i in range(len(xs)):
            for p in perms(xs[:i] + xs[i + 1:]):
                yield [xs[i]] + p

    cycles_from(frozenset(range(n)), [])
    return out


def ham_cycles(n, adj):
    """All Hamilton cycles (as edge sets), each once."""
    res = []
    path = [0]
    seen = {0}

    def rec():
        v = path[-1]
        if len(path) == n:
            if 0 in adj[v] and path[1] < path[-1]:
                res.append(frozenset(tuple(sorted((path[i], path[(i + 1) % n]))) for i in range(n)))
            return
        for w in adj[v]:
            if w not in seen:
                seen.add(w); path.append(w)
                rec()
                path.pop(); seen.discard(w)

    rec()
    return res


def main():
    n, M = int(sys.argv[1]), int(sys.argv[2])
    H = frozenset(tuple(sorted((i, (i + 1) % n))) for i in range(n))
    pairs = 0
    ghist, lochist = Counter(), Counter()
    rigid = 0
    for F in two_factors(n):
        S = F & H
        if len(S) != M or (0, 1) not in S:
            continue
        verts = [v for e in S for v in e]
        if len(set(verts)) != 2 * M:              # stretches must be single, disjoint edges
            continue
        pairs += 1
        G = F | H
        adj = {v: set() for v in range(n)}
        for a, b in G:
            adj[a].add(b); adj[b].add(a)
        unshared = H - S
        good = [C for C in ham_cycles(n, adj) if not unshared <= C]
        ghist[len(good)] += 1
        if not good:
            rigid += 1
        else:
            lochist[min(len(C - H) for C in good)] += 1
    print(f"INDEP n={n} M={M} pairs={pairs} rigid={rigid}")
    for g in sorted(ghist):
        print(f"HIST {g} {ghist[g]}")
    for t in sorted(lochist):
        print(f"LOCHIST {t} {lochist[t]}")


if __name__ == "__main__":
    main()
