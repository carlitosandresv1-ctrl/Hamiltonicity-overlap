import itertools, subprocess, sys, collections
HC = sys.argv[1]
def E(a,b): return (min(a,b),max(a,b))
def two_factors(n):
    adj=[set() for _ in range(n)]; deg=[0]*n
    def rec(v):
        while v<n and deg[v]==2: v+=1
        if v==n: yield {E(a,b) for a in range(n) for b in adj[a] if a<b}; return
        need=2-deg[v]
        for ws in itertools.combinations([w for w in range(v+1,n) if deg[w]<2 and w not in adj[v]],need):
            for w in ws: adj[v].add(w); adj[w].add(v); deg[w]+=1
            deg[v]+=need; yield from rec(v+1); deg[v]-=need
            for w in ws: adj[v].discard(w); adj[w].discard(v); deg[w]-=1
    yield from rec(0)
def run(n, edges, F):
    inp=f"{n} {len(edges)}\n"+"".join(f"{a} {b}\n" for a,b in edges)+f"{len(F)}\n"+"".join(f"{a} {b}\n" for a,b in F)
    c,ov=subprocess.run([HC],input=inp,capture_output=True,text=True).stdout.split(); return int(c),int(ov)
def pattern(n,S):
    start=next(i for i in range(n) if E(i,(i+1)%n) not in S)
    sz=[];L=0
    for k in range(1,n+1):
        i=(start+k)%n
        if E(i,(i+1)%n) in S: L+=1
        elif L: sz.append(L); L=0
    if L: sz.append(L)
    return tuple(sorted(sz))
for n in range(6,10):
    H={E(i,(i+1)%n) for i in range(n)}; res=collections.Counter()
    for F in two_factors(n):
        S=F&H
        if not 1<=len(S)<=4: continue
        c,ov=run(n,sorted(F|H),sorted(F))
        if ov==len(S): res[(len(S),pattern(n,S),c)]+=1
    print(f"n={n} rigid pairs with 1<=s<=4  (s, pattern, #HC): count ->", dict(res))
