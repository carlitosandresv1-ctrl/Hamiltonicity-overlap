import networkx as nx, json
from k3 import analyze
fams=[
 ("K_5",nx.complete_graph(5)),("K_6",nx.complete_graph(6)),("K_7",nx.complete_graph(7)),("K_8",nx.complete_graph(8)),
 ("K_{3,3}",nx.complete_bipartite_graph(3,3)),("K_{4,4}",nx.complete_bipartite_graph(4,4)),
 ("Petersen",nx.petersen_graph()),("Q_3 (cubo)",nx.hypercube_graph(3)),("Q_4",nx.hypercube_graph(4)),
 ("C_9(1,2)",nx.circulant_graph(9,[1,2])),("C_10(1,2)",nx.circulant_graph(10,[1,2])),
 ("C_10(1,3)",nx.circulant_graph(10,[1,3])),("Wagner V_8",nx.circulant_graph(8,[1,4])),
 ("K_{3,4}",nx.complete_bipartite_graph(3,4)),
]
for name,G in fams:
    G=nx.convert_node_labels_to_integers(G)
    r=analyze(G,kmax=3)
    print(f"{name:12s} n={G.number_of_nodes():2d} |F|={r['nTF']:5d} comp(X_2)={r['comp2']:4d} b1(X_2)={r['b1_2']:6d} ham={r['ham']} M*_2={r['Ms2']} M*_3={r['Ms3']}")
