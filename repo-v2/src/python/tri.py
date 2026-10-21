import sys, json, networkx as nx
from lib import two_factors, ncyc
from local import ciclos_de
def test(G):
    """2-factores formados solo por triangulos: ¿existe H que conserve 2 aristas de cada uno?"""
    n=G.number_of_nodes(); TF=[set(F) for F in two_factors(G)]
    Hs=[F for F in TF if ncyc(n,F)==1]
    if not Hs: return None
    casos=0
    for F in TF:
        Cs=ciclos_de(n,F)
        if len(Cs)<2 or any(len(C)!=3 for C in Cs): continue
        casos+=1
        if not any(all(len(C-h)<=1 for C in Cs) for h in Hs):
            return ('FALLA',casos)
    return ('ok',casos)
tot=0; casos=0; fallos=[]
for line in sys.stdin:
    g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
    r=test(G)
    if r is None: continue
    tot+=1; casos+=r[1]
    if r[0]=='FALLA':
        fallos.append(g6)
        if len(fallos)<=3: print('CONTRAEJEMPLO (factor de triangulos):',g6,flush=True)
print(json.dumps(dict(grafos=tot, dos_factores_de_triangulos=casos, fallos=len(fallos))))
