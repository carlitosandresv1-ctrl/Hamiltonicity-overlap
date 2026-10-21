import itertools as it, networkx as nx
from lib import two_factors, ncyc

def circuitos(F, H, pairing_choice):
    """Dado F,H (conjuntos de aristas) y una eleccion de emparejamiento local en cada
    vertice de grado 4, devuelve los circuitos alternantes y su tamaño en aristas de F."""
    DF = F - H; DH = H - F
    inc = {}
    for e in DF | DH:
        for v in e: inc.setdefault(v, {'F': [], 'H': []})
        for v in e: inc[v]['F' if e in DF else 'H'].append(e)
    # emparejamiento local: partner[(v,e)] = arista que sigue al pasar por v
    partner = {}
    deg4 = sorted(v for v in inc if len(inc[v]['F']) == 2)
    for v in inc:
        fs, hs = inc[v]['F'], inc[v]['H']
        if len(fs) == 1:
            partner[(v, fs[0])] = hs[0]; partner[(v, hs[0])] = fs[0]
        else:
            k = pairing_choice[deg4.index(v)]
            a, b = (hs[0], hs[1]) if k == 0 else (hs[1], hs[0])
            partner[(v, fs[0])] = a; partner[(v, a)] = fs[0]
            partner[(v, fs[1])] = b; partner[(v, b)] = fs[1]
    vistas = set(); circ = []
    for e0 in DF | DH:
        if e0 in vistas: continue
        c = set(); e = e0; v = e[1]
        while True:
            c.add(e); vistas.add(e)
            e2 = partner[(v, e)]
            v = e2[0] + e2[1] - v
            e = e2
            if e in c and e == e0: break
            if e in c: break
        circ.append(c)
    return circ

def beta_par(F, H, cap=1024):
    """min sobre sistemas de transicion del mayor |C ∩ F|"""
    DF = F - H; DH = H - F
    inc = {}
    for e in DF | DH:
        for v in e: inc.setdefault(v, {'F': [], 'H': []})
        for v in e: inc[v]['F' if e in DF else 'H'].append(e)
    deg4 = [v for v in inc if len(inc[v]['F']) == 2]
    if 2**len(deg4) > cap:
        opciones = [tuple(0 for _ in deg4)]          # demasiados: solo una muestra
    else:
        opciones = list(it.product((0, 1), repeat=len(deg4)))
    mejor = 10**9
    for ch in opciones:
        circ = circuitos(F, H, ch)
        m = max(len(c & F) for c in circ)
        mejor = min(mejor, m)
    return mejor, len(deg4)

def toggle(F, C):
    """intercambia un circuito: quita C∩F y pone C∖F"""
    return (F - C) | (C - F)
