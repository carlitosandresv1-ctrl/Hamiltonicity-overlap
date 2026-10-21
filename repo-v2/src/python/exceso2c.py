import networkx as nx, random, sys, json
from maxov import max_overlap
from lib import ncyc
def arranque(n,c,rng,extra):
    G=nx.Graph(); G.add_nodes_from(range(n)); F=set()
    perm=list(range(n)); rng.shuffle(perm); tam=n//c
    for k in range(c):
        blo=perm[k*tam:(k+1)*tam] if k<c-1 else perm[(c-1)*tam:]
        for j in range(len(blo)):
            a,b=blo[j],blo[(j+1)%len(blo)]; e=(min(a,b),max(a,b)); F.add(e); G.add_edge(*e)
    libres=[e for e in nx.non_edges(G)]; rng.shuffle(libres)
    G.add_edges_from(libres[:extra])
    return G,F
def val(G,F,c):
    n=G.number_of_nodes()
    if not nx.is_connected(G): return None
    m=max_overlap(G,F)
    return None if m is None else (n-m)-2*c
n=int(sys.argv[1]); c=int(sys.argv[2]); rng=random.Random(int(sys.argv[3])); iters=int(sys.argv[4])
mejor=-99; arg=None
for r in range(5):
    G,F=arranque(n,c,rng,rng.randint(3,10)); cur=val(G,F,c)
    if cur is None: continue
    for t in range(iters):
        H=G.copy()
        noF=[e for e in H.edges() if (min(e),max(e)) not in F]
        libres=[e for e in nx.non_edges(H)]
        if rng.random()<0.5 and noF: H.remove_edge(*rng.choice(noF))
        elif libres: H.add_edge(*rng.choice(libres))
        s=val(H,F,c)
        if s is not None and s>=cur: G,cur=H,s
        if s is not None and s>mejor: mejor=s; arg=nx.to_graph6_bytes(G,header=False).strip().decode()
print(json.dumps(dict(n=n,c=c,max_cor_menos_2c=mejor,grafo=arg)))
