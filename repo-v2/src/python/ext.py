import sys
from protegidas import todos_2factores, ciclos_ham
from familia import familia
n=int(sys.argv[1])
H=frozenset((min(i,(i+1)%n),max(i,(i+1)%n)) for i in range(n))
Fn,_=familia(n); Fn=frozenset(Fn)
orb=set()
for sh in range(n):
    for d in (1,-1):
        orb.add(frozenset((min((u*d+sh)%n,(v*d+sh)%n),max((u*d+sh)%n,(v*d+sh)%n)) for (u,v) in Fn))
ext=[]
for F in todos_2factores(n):
    hs=ciclos_ham(n,F|H)
    if not hs: continue
    if max(len(F&T) for T in hs)==5: ext.append((F,len(hs)))
uh=[F for F,h in ext if h==1]
print("n=",n,"extremales(ov=5):",len(ext)," copias de Gamma_n:",sum(1 for F,h in ext if F in orb),
      " de ellos UH:",len(uh)," todos los UH son copias de Gamma_n?",all(F in orb for F in uh))
