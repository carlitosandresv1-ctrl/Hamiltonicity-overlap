"""Fija s=|F cap H|=4 y minimiza el numero de ciclos hamiltonianos de Gamma=F u H.
Si alcanza 1, existe una union UH con s=4 y ov(n)<=4: la conjetura es falsa."""
import sys, random
from buscaUH import nham, adyacencia, grados_ok

def arranque(n, rng, s_obj):
    """2-factor con exactamente s_obj aristas compartidas, tramos unitarios"""
    for _ in range(4000):
        comp = sorted(rng.sample(range(n), s_obj))          # aristas (i,i+1) compartidas
        if any((comp[k+1]-comp[k]) == 1 for k in range(len(comp)-1)): continue
        if comp[0]==0 and comp[-1]==n-1: continue
        F = set((c,(c+1)%n) for c in comp)
        libres = [v for v in range(n) if all(v not in e for e in F)]
        # emparejar los extremos de los tramos y los libres en ciclos
        gr = {}
        for (u,v) in F: gr[u]=gr.get(u,0)+1; gr[v]=gr.get(v,0)+1
        pend = [v for v in range(n) if gr.get(v,0) < 2]
        rng.shuffle(pend)
        ok=True; G=set(F)
        # cadena aleatoria sobre los pendientes (cada uno necesita 2-gr aristas)
        need = {v: 2-gr.get(v,0) for v in range(n)}
        orden = [v for v in range(n) for _ in range(need[v])]
        rng.shuffle(orden)
        G2=set(G); need2=dict(need)
        for _ in range(300):
            cand=[v for v in range(n) if need2[v]>0]
            if not cand: break
            u=rng.choice(cand)
            opc=[w for w in range(n) if w!=u and need2[w]>0 and (min(u,w),max(u,w)) not in G2
                 and abs(u-w) not in (1,) and not (min(u,w)==0 and max(u,w)==n-1)]
            if not opc: ok=False; break
            w=rng.choice(opc); e=(min(u,w),max(u,w))
            G2.add(e); need2[u]-=1; need2[w]-=1
        if not ok or any(need2[v]!=0 for v in range(n)) or len(G2)!=n: continue
        if not grados_ok(n,G2,None): continue
        # debe ser 2-regular con ciclos de longitud >=3 (simple ya garantizado)
        return G2
    return None

def main(n, iters, reinicios):
    rng = random.Random(20261007+n)
    H = set((min(i,(i+1)%n),max(i,(i+1)%n)) for i in range(n))
    mejor = 10**9; argm=None
    for r in range(reinicios):
        F = arranque(n, rng, 4)
        if F is None: continue
        cur = nham(n, adyacencia(n, F|H), tope=40)
        if cur == 0: continue
        for t in range(iters):
            Fl = sorted(F)
            i,j = rng.randrange(n), rng.randrange(n)
            if i==j: continue
            (a,b),(c,d) = Fl[i],Fl[j]
            if len({a,b,c,d})<4: continue
            for (x1,y1),(x2,y2) in (((a,c),(b,d)),((a,d),(b,c))):
                e1=(min(x1,y1),max(x1,y1)); e2=(min(x2,y2),max(x2,y2))
                if e1 in F or e2 in F: continue
                G=set(F); G.discard(Fl[i]); G.discard(Fl[j]); G.add(e1); G.add(e2)
                if len(G)!=n or not grados_ok(n,G,None): continue
                if len(G & H)!=4: continue              # mantiene s=4
                v = nham(n, adyacencia(n,G|H), tope=40)
                if v>=1 and v<=cur:
                    F,cur=G,v
                    if cur<mejor:
                        mejor=cur; argm=sorted(F)
                        print(f"  n={n}  s=4  #ciclos ham = {cur}", flush=True)
                        if cur==1: print("  *** UNION UH CON s=4:",argm, flush=True); return 1
                break
    print(f"n={n}: minimo #ciclos ham con s=4 = {mejor}")
    return mejor

if __name__=="__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
