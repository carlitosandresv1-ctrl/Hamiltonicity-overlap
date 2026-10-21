"""Busqueda de un 'bloque 4-regular con puertos'.

Queremos un grafo G0 con m vertices tal que:
  - exactamente dos vertices x,y tienen grado 2 y el resto grado 4;
  - hay EXACTAMENTE UN camino Hamiltoniano de x a y.

Si existe, al enchufar dos patas en x y dos en y se obtiene un bloque cuyos
vertices son todos de grado 4 y cuyo unico modo de atravesarlo es entrar por
una pata de x y salir por una de y, con ruta interna unica.  Sustituyendo cada
tramo de S por una copia, Gamma se convierte en un grafo 4-regular cuyos ciclos
Hamiltonianos estan en biyeccion con los de Gamma que contienen S, y la
conjetura de Sheehan implicaria la hipotesis del motor de iteracion.

La unicidad es imprescindible: si hubiera dos rutas internas, un 'segundo'
ciclo Hamiltoniano del grafo 4-regular podria diferir solo dentro del bloque y
no dar un segundo ciclo en Gamma.
"""
import sys
import networkx as nx


def caminos_ham(G, x, y, tope=2):
    """cuenta caminos Hamiltonianos de x a y, parando en 'tope'."""
    n = G.number_of_nodes()
    ady = {v: list(G.neighbors(v)) for v in G}
    total = 0
    vis = {v: False for v in G}
    vis[x] = True

    def dfs(v, k):
        nonlocal total
        if total >= tope:
            return
        if k == n:
            if v == y:
                total += 1
            return
        if v == y:
            return                      # llegaria a y antes de cubrir todo
        for w in ady[v]:
            if vis[w]:
                continue
            vis[w] = True
            dfs(w, k + 1)
            vis[w] = False

    dfs(x, 1)
    return total


def examina(g6):
    G = nx.from_graph6_bytes(g6.encode())
    d = dict(G.degree())
    g2 = [v for v in d if d[v] == 2]
    if len(g2) != 2:
        return None
    if any(d[v] != 4 for v in d if d[v] != 2):
        return None
    x, y = g2
    c = caminos_ham(G, x, y, tope=2)
    if c == 1:
        return (g6, x, y)
    return None


if __name__ == "__main__":
    hallados = 0
    examinados = 0
    for linea in sys.stdin:
        g6 = linea.strip()
        if not g6:
            continue
        examinados += 1
        r = examina(g6)
        if r:
            hallados += 1
            if hallados <= 5:
                print("GADGET:", r[0], " x,y =", r[1], r[2], flush=True)
    print(f"  examinados={examinados}  gadgets={hallados}")
