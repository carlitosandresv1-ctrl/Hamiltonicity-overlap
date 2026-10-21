"""Cuenta ciclos hamiltonianos de G = F u H por backtracking.
En grafos con Delta <= 4 y vertices forzados el arbol de busqueda es minusculo."""
import sys
from familia import familia


def cuenta_ham(n, E, tope=10):
    ady = [[] for _ in range(n)]
    for (u, v) in E:
        ady[u].append(v)
        ady[v].append(u)
    total = 0
    vis = [False] * n
    vis[0] = True
    cam = [0]

    def dfs(v):
        nonlocal total
        if total >= tope:
            return
        if len(cam) == n:
            if 0 in ady[v]:
                total += 1
            return
        for w in ady[v]:
            if vis[w]:
                continue
            # evita contar cada ciclo en sus dos sentidos
            if len(cam) == 1 and w > ady[0][-1]:
                pass
            vis[w] = True
            cam.append(w)
            dfs(w)
            cam.pop()
            vis[w] = False

    dfs(0)
    return total // 2          # cada ciclo se recorre en dos sentidos


if __name__ == "__main__":
    hasta = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    print(" n   |F cap H|   #ciclos ham   cor(F)   n-5   ok")
    for n in range(10, hasta + 1):
        F, H = familia(n)
        G = F | H
        s = len(F & H)
        nh = cuenta_ham(n, G)
        cor = n - s if nh == 1 else None
        print(f"{n:3d} {s:9d} {nh:13d} {str(cor):>8} {n-5:5d}   "
              f"{'SI' if (nh == 1 and s == 5) else 'NO'}")
