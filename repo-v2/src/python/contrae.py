"""Contraccion Gamma/S con S = F cap H.

Los bloques son las componentes del subgrafo S (caminos de H). Hay n-s bloques.
Toda arista de Gamma que no este en S se convierte en arista entre bloques
(bucle si ambos extremos caen en el mismo bloque).

Grado de un bloque B:  suma de grados en Gamma menos 2 por cada arista de S
interna.  Para un tramo de longitud l: dos extremos de grado 3 y l-1 interiores
de grado 2, es decir 2l+4, menos 2l, igual a 4.  Para un bloque unitario, 4.
Luego Gamma/S es 4-regular, con los bucles contando 2.
"""


def bloques(n, S):
    padre = list(range(n))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for (u, v) in S:
        padre[raiz(u)] = raiz(v)
    rep = {}
    idb = [0] * n
    for v in range(n):
        r = raiz(v)
        if r not in rep:
            rep[r] = len(rep)
        idb[v] = rep[r]
    return idb, len(rep)


def contrae(n, E, S):
    """devuelve (nb, aristas, bucles_por_bloque, grados)"""
    idb, nb = bloques(n, S)
    aristas = []
    bucles = [0] * nb
    grados = [0] * nb
    for (u, v) in E:
        if (u, v) in S:
            continue
        a, b = idb[u], idb[v]
        if a == b:
            bucles[a] += 1
            grados[a] += 2
        else:
            aristas.append((a, b))
            grados[a] += 1
            grados[b] += 1
    return nb, aristas, bucles, grados


def simple(nb, aristas, bucles):
    if sum(bucles):
        return False
    vistas = set()
    for (a, b) in aristas:
        k = (min(a, b), max(a, b))
        if k in vistas:
            return False
        vistas.add(k)
    return True


if __name__ == "__main__":
    from familia import familia
    for n in (11, 12, 13, 16, 20):
        F, H = familia(n)
        S = F & H
        nb, ar, bu, gr = contrae(n, F | H, S)
        print(f"n={n}: s={len(S)}  bloques={nb} (n-s={n-len(S)})  "
              f"grados={sorted(set(gr))}  bucles={sum(bu)}  simple={simple(nb,ar,bu)}")
