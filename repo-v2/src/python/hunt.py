import networkx as nx, random, sys, json
from local import cumple_local
random.seed(int(sys.argv[1]))
nmax=int(sys.argv[2]); lim=int(sys.argv[3])
fallos=0; tot=0
for t in range(lim):
    n=random.choice([9,10,nmax])
    p=random.uniform(0.3,0.6)
    G=nx.gnp_random_graph(n,p,seed=random.randint(0,10**7))
    if not nx.is_connected(G) or min(d for _,d in G.degree())<2: continue
    try: r=cumple_local(G)
    except RecursionError: continue
    if r is None: continue
    tot+=1
    if not r[0]:
        fallos+=1; print('CONTRAEJEMPLO', nx.to_graph6_bytes(G,header=False).strip().decode(), r[1], flush=True); break
print(json.dumps(dict(examinados=tot,fallos=fallos)))
