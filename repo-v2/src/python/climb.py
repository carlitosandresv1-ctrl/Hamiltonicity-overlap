import random, math, sys, networkx as nx
from lib import kstar, two_factors
def score(G):
    n=G.number_of_nodes()
    if not nx.is_connected(G): return -99, None
    try: r=kstar(G)
    except RecursionError: return -99,None
    if r['kstar'] is None: return -99,None
    return r['kstar']-math.ceil(n/2), r
def mutate(G, maxdeg):
    H=G.copy(); E=list(H.edges()); nonE=[(u,v) for u,v in nx.non_edges(H)]
    for _ in range(40):
        H2=G.copy()
        if E and nonE and random.random()<0.7:
            e=random.choice(E); f=random.choice(nonE)
            H2.remove_edge(*e); H2.add_edge(*f)
        elif random.random()<0.5 and nonE:
            H2.add_edge(*random.choice(nonE))
        elif E:
            H2.remove_edge(*random.choice(E))
        if max((d for _,d in H2.degree()), default=0)<=maxdeg and min((d for _,d in H2.degree()),default=0)>=2:
            return H2
    return G
random.seed(int(sys.argv[3]) if len(sys.argv)>3 else 0)
n=int(sys.argv[1]); maxdeg=int(sys.argv[2]); iters=int(sys.argv[4]) if len(sys.argv)>4 else 300
best=-99; bestG=None
for restart in range(6):
    G=nx.random_regular_graph(min(maxdeg,4), n, seed=random.randint(0,10**6)) if (n*min(maxdeg,4))%2==0 else nx.cycle_graph(n)
    cur,_=score(G)
    for it in range(iters):
        H=mutate(G,maxdeg); s,r=score(H)
        if s>=cur: G,cur=H,s
        if s>best and r: best=s; bestG=(nx.to_graph6_bytes(H,header=False).strip().decode(), r)
print('n=',n,'Δ<=',maxdeg,'mejor margen k*-ceil(n/2) =',best, bestG)
