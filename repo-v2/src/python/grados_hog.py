"""Lee las listas graph6 de House of Graphs y calcula, para cada grafo UH,
el grado maximo, n2, n3 y el peso n3 + 2*n2 relevante para la escalera.

Un contraejemplo a ov(n) >= 5 con s <= 4 debe ser un grafo UH con
grado maximo <= 4 y peso n3 + 2 n2 <= 8.
"""
import sys
from collections import Counter


def g6(linea):
    s = linea.strip()
    if not s:
        return None
    if s[0] == ':' or s[0] == '&':
        raise ValueError("formato sparse6/digraph6 no soportado")
    # orden
    if ord(s[0]) - 63 < 63:
        n = ord(s[0]) - 63
        resto = s[1:]
    elif s[1] != '~':
        n = 0
        for c in s[1:4]:
            n = n * 64 + (ord(c) - 63)
        resto = s[4:]
    else:
        n = 0
        for c in s[2:8]:
            n = n * 64 + (ord(c) - 63)
        resto = s[8:]
    bits = []
    for c in resto:
        v = ord(c) - 63
        for k in range(5, -1, -1):
            bits.append((v >> k) & 1)
    E = []
    pos = 0
    for j in range(1, n):
        for i in range(j):
            if pos < len(bits) and bits[pos]:
                E.append((i, j))
            pos += 1
    return n, E


def perfil(n, E):
    g = [0] * n
    for (u, v) in E:
        g[u] += 1
        g[v] += 1
    c = Counter(g)
    return max(g), min(g), c


def main(ruta):
    filas = []
    for linea in open(ruta):
        r = g6(linea)
        if r is None:
            continue
        n, E = r
        dmax, dmin, c = perfil(n, E)
        peso = c[3] + 2 * c[2]
        filas.append((n, dmax, dmin, c[2], c[3], c[4], peso, len(E)))
    filas.sort()
    print(f"{'n':>3} {'Dmax':>4} {'dmin':>4} {'n2':>3} {'n3':>3} {'n4':>3} {'peso':>4} {'|E|':>4}")
    for f in filas:
        print(f"{f[0]:>3} {f[1]:>4} {f[2]:>4} {f[3]:>3} {f[4]:>3} {f[5]:>3} {f[6]:>4} {f[7]:>4}")
    print()
    print(f"total grafos: {len(filas)}")
    conDmax4 = [f for f in filas if f[1] <= 4]
    print(f"con grado maximo <= 4: {len(conDmax4)}")
    peligro = [f for f in filas if f[1] <= 4 and f[6] <= 8]
    print(f"con grado maximo <= 4 y peso <= 8 (contraejemplos): {len(peligro)}")
    if filas:
        print(f"peso minimo observado entre todos: {min(f[6] for f in filas)}")
    print(f"n3 minimo observado: {min(f[4] for f in filas)}")


if __name__ == "__main__":
    main(sys.argv[1])
