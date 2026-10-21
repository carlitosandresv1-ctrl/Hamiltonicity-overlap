"""La familia extremal explicita  (G_n, F_n)  con |F cap H| = 5.

H = (0,1,...,n-1).
F = triangulo {1,2,3}  u  ciclo largo  (0, Z, 4, 5, 6)
donde Z es el zigzag sobre el intervalo [7, n-1]:

      Z = 7, n-1, 8, n-2, 9, n-3, ...

es decir  z_{2i} = 7+i,  z_{2i+1} = n-1-i,  hasta cubrir [7,n-1].
"""


def zigzag(n):
    izq, der = 7, n - 1
    out = []
    while izq <= der:
        out.append(izq)
        if izq != der:
            out.append(der)
        izq += 1
        der -= 1
    return out


def familia(n):
    """devuelve (F, H) como conjuntos de aristas normalizadas"""
    assert n >= 10
    Z = zigzag(n)
    largo = [0] + Z + [4, 5, 6]
    assert sorted(largo) == [0] + list(range(4, n)), (n, sorted(largo))
    F = {(1, 2), (2, 3), (1, 3)}
    for i in range(len(largo)):
        a, b = largo[i], largo[(i + 1) % len(largo)]
        F.add((min(a, b), max(a, b)))
    H = set((min(i, (i + 1) % n), max(i, (i + 1) % n)) for i in range(n))
    assert len(F) == n, (n, len(F))
    return F, H


if __name__ == "__main__":
    for n in range(10, 20):
        F, H = familia(n)
        print(f"n={n:3d}  |F cap H| = {len(F & H)}   F cap H = {sorted(F & H)}")
