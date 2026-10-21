"""Segunda familia: triangulos {1,2,3} y {5,6,7}, mas un ciclo largo sobre
   {0,4} u [8,n-1].  Probamos varios patrones para el ciclo largo."""
import sys
from buscaUH import nham, adyacencia

def zz(a,b):
    izq,der=a,b; out=[]
    while izq<=der:
        out.append(izq)
        if izq!=der: out.append(der)
        izq+=1; der-=1
    return out

def patrones(n):
    R=list(range(8,n))
    yield "0,4,zz(8..n-1)",      [0,4]+zz(8,n-1)
    yield "0,4,zz desde 9",      [0,4]+([9]+zz(10,n-1)+[8] if n>=11 else [9,8])
    yield "0,4,rev zz",          [0,4]+zz(8,n-1)[::-1]
    yield "0,zz,4",              [0]+zz(8,n-1)+[4]

def construye(n, seq):
    F={(1,2),(2,3),(1,3),(5,6),(6,7),(5,7)}
    for i in range(len(seq)):
        a,b=seq[i],seq[(i+1)%len(seq)]
        F.add((min(a,b),max(a,b)))
    return F

for n in range(10,23):
    H=set((min(i,(i+1)%n),max(i,(i+1)%n)) for i in range(n))
    res=[]
    for nombre,seq in patrones(n):
        if sorted(seq)!=sorted([0,4]+list(range(8,n))): continue
        F=construye(n,seq)
        g={}
        for (u,v) in F: g[u]=g.get(u,0)+1; g[v]=g.get(v,0)+1
        if len(F)!=n or any(g.get(v,0)!=2 for v in range(n)): continue
        nh=nham(n,adyacencia(n,F|H),tope=6)
        res.append((nombre,len(F&H),nh))
    print(f"n={n}: "+" | ".join(f"{a}: s={b}, #ham={c}" for a,b,c in res))
