for m in 12 13; do e=$((2*m-2))
  c=$(nauty-geng -q -c -d2 -D4 $m $e:$e 2>/dev/null | python -c "
import sys, networkx as nx
k=0
for l in sys.stdin:
    G=nx.from_graph6_bytes(l.strip().encode()); d=dict(G.degree())
    if sum(1 for v in d if d[v]==2)==2 and all(d[v] in (2,4) for v in d): k+=1
print(k)")
  echo "m=$m: $c"
done
