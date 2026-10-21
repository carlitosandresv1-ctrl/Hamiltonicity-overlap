import sys
from protegidas import todos_2factores, ciclos_ham
from familia import familia
n=int(sys.argv[1])
H=frozenset((min(i,(i+1)%n),max(i,(i+1)%n)) for i in range(n))
Fn,_=familia(n); Fn=frozenset(Fn)
def orb(F):
    o=set()
    for sh in range(n):
        for d in (1,-1):
            o.add(frozenset((min((u*d+sh)%n,(v*d+sh)%n),max((u*d+sh)%n,(v*d+sh)%n)) for (u,v) in F))
    return o
orbG=orb(Fn)
uh=[]
for F in todos_2factores(n):
    hs=ciclos_ham(n,F|H)
    if not hs: continue
    if max(len(F&T) for T in hs)!=5 or len(hs)!=1: continue
    uh.append(F)
clases=[]
for F in uh:
    if not any(F in c for c in clases): clases.append(orb(F))
print(f"n={n}: pares UH extremales={len(uh)}, clases={len(clases)}, de ellas Gamma_n={sum(1 for c in clases if Fn in c)}")
def ciclosF(F):
    ady={v:[] for v in range(n)}
    for (u,v) in F: ady[u].append(v); ady[v].append(u)
    vis=set(); out=[]
    for s0 in range(n):
        if s0 in vis: continue
        c=[s0]; vis.add(s0); prev=None; cur=s0
        while True:
            sig=[w for w in ady[cur] if w!=prev]
            if not sig or sig[0]==s0: break
            prev,cur=cur,sig[0]; c.append(cur); vis.add(cur)
        out.append(c)
    return out
for i,c in enumerate(clases):
    F=sorted(c)[0]
    print(f"  clase {i+1} (|orbita|={len(c)}){'  = Gamma_n' if Fn in c else ''}:")
    print(f"    F={sorted(F)}  S={sorted(F&H)}  ciclos de F={ciclosF(F)}")
