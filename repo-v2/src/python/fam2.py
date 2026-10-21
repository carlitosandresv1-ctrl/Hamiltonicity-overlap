"""Segunda familia candidata: dos triangulos colgados y un ciclo que trenza.
   T1={0,1,2} con cuerda 0-2, T2={6,7,8} con cuerda 6-8, y el resto
   {3,4,5} u {9..n-1} en un ciclo con la unica arista compartida (4,5)."""
import sys
from buscaUH import nham, adyacencia

def construye(n, patron):
    F={(0,1),(1,2),(0,2),(6,7),(7,8),(6,8)}
    resto=[3,4,5]+list(range(9,n))
    # patron: orden ciclico del resto
    seq=patron(n,resto)
    assert sorted(seq)==sorted(resto), (seq,resto)
    for i in range(len(seq)):
        a,b=seq[i],seq[(i+1)%len(seq)]
        F.add((min(a,b),max(a,b)))
    return F

def zig(n,resto):
    # 3, luego zigzag sobre [9,n-1], luego 4,5   (analogo a Gamma_n)
    izq,der=9,n-1; Z=[]
    while izq<=der:
        Z.append(izq)
        if izq!=der: Z.append(der)
        izq+=1; der-=1
    return [3]+Z+[4,5]

n0=int(sys.argv[1]); n1=int(sys.argv[2])
for n in range(n0,n1+1):
    H=set((min(i,(i+1)%n),max(i,(i+1)%n)) for i in range(n))
    try: F=construye(n,zig)
    except AssertionError as e: print(n,"patron invalido"); continue
    g={}
    for (u,v) in F: g[u]=g.get(u,0)+1; g[v]=g.get(v,0)+1
    if len(F)!=n or any(g.get(v,0)!=2 for v in range(n)):
        print(f"n={n}: no es 2-factor (|F|={len(F)})"); continue
    nh=nham(n,adyacencia(n,F|H),tope=6)
    print(f"n={n}: |F cap H|={len(F&H)}  #ciclos ham={nh}  {'UH' if nh==1 else ''}")
