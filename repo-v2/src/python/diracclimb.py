import networkx as nx, random, sys, json, math
from maxov import max_overlap
def arranque(n,c,rng):
    G=nx.Graph(); G.add_nodes_from(range(n)); F=set()
    perm=list(range(n)); rng.shuffle(perm); tam=n//c
    for k in range(c):
        blo=perm[k*tam:(k+1)*tam] if k<c-1 else perm[(c-1)*tam:]
        for j in range(len(blo)):
            a,b=blo[j],blo[(j+1)%len(blo)]; e=(min(a,b),max(a,b)); F.add(e); G.add_edge(*e)
    d=math.ceil(n/2)
    libres=[e for e in nx.non_edges(G)]; rng.shuffle(libres)
    for e in libres:
        if min(x for _,x in G.degree())>=d: break
        if G.degree(e[0])<d or G.degree(e[1])<d: G.add_edge(*e)
    return G,F
def score(G,F,c):
    n=G.number_of_nodes(); d=math.ceil(n/2)
    if min(x for _,x in G.degree())<d or not nx.is_connected(G): return None
    m=max_overlap(G,F)
    return None if m is None else (n-m)-c
n=int(sys.argv[1]); c=int(sys.argv[2]); rng=random.Random(int(sys.argv[3])); iters=int(sys.argv[4])
mejor=-1; arg=None
for restart in range(5):
    G,F=arranque(n,c,rng); cur=score(G,F,c)
    if cur is None: continue
    for t in range(iters):
        H=G.copy()
        noF=[e for e in H.edges() if (min(e),max(e)) not in F]
        libres=[e for e in nx.non_edges(H)]
        if rng.random()<0.6 and noF: H.remove_edge(*rng.choice(noF))
        elif libres: H.add_edge(*rng.choice(libres))
        s=score(H,F,c)
        if s is not None and s>=cur: G,cur=H,s
        if s is not None and s>mejor: mejor=s; arg=nx.to_graph6_bytes(G,header=False).strip().decode()
print(json.dumps(dict(n=n,c=c,exceso_max=mejor,grafo=arg)))
