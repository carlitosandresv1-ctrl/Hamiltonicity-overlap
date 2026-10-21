"""Segunda familia extremal Delta_n  (n >= 10).

H = (0,1,...,n-1).  Zigzag sobre [8, n-1]:  z_{2i} = 8+i,  z_{2i+1} = n-1-i.
Delta_n:   F = triangulo {1,2,3}  u  triangulo {5,6,7}
                u  ciclo (0, z_0, z_1, ..., z_{L-1}, 4),   L = n-8.
"""
def zigzag(a,b):
    izq,der=a,b; out=[]
    while izq<=der:
        out.append(izq)
        if izq!=der: out.append(der)
        izq+=1; der-=1
    return out

def delta(n):
    assert n>=10
    Z=zigzag(8,n-1)
    largo=[0]+Z+[4]
    assert sorted(largo)==[0,4]+list(range(8,n)), (n,sorted(largo))
    F={(1,2),(2,3),(1,3),(5,6),(6,7),(5,7)}
    for i in range(len(largo)):
        a,b=largo[i],largo[(i+1)%len(largo)]
        F.add((min(a,b),max(a,b)))
    H=set((min(i,(i+1)%n),max(i,(i+1)%n)) for i in range(n))
    assert len(F)==n, (n,len(F))
    return F,H

if __name__=="__main__":
    import sys
    from buscaUH import nham, adyacencia
    from forzado import propaga
    print(" n  |F cap H|  #ciclos ham  grados(n2,n3,n4)  forzado cierra?")
    for n in range(10, (int(sys.argv[1]) if len(sys.argv) > 1 else 20) + 1):
        F,H=delta(n)
        G=F|H
        d={}
        for (u,v) in G: d[u]=d.get(u,0)+1; d[v]=d.get(v,0)+1
        n2=sum(1 for v in range(n) if d[v]==2); n3=sum(1 for v in range(n) if d[v]==3)
        n4=sum(1 for v in range(n) if d[v]==4)
        nh=nham(n,adyacencia(n,G),tope=5)
        forz,_=propaga(n,G)
        print(f"{n:3d} {len(F&H):8d} {nh:12d}      ({n2},{n3},{n4})        {'SI' if forz==H else 'NO'}")
