# Solapamiento garantizado entre un 2-factor y un ciclo hamiltoniano

Código, datos y verificaciones del artículo *Guaranteed overlap between a
2-factor and a Hamilton cycle* (C. Velásquez, Madrid, 2026), junto con el
material de la fase anterior del proyecto.

## El problema

Sea `G` un grafo hamiltoniano con `n` vértices y `F` un 2-factor de `G`.
Se define

```
ov_G(F) = max |F ∩ H|   sobre los ciclos hamiltonianos H de G
cor_G(F) = n − ov_G(F)
ov(n)    = min ov_G(F)  sobre todos los pares (G,F) con |V(G)| = n
```

El teorema de reducción concentra el problema en los grafos que son unión de un
2-factor y un ciclo hamiltoniano, `Γ = F ∪ H`, con `H` fijo al ciclo canónico
`(0,1,…,n−1)`. Todo el código de este repositorio trabaja en esa normalización:
un par se representa por el 2-factor `F`, y `H` está implícito.

Notación constante en el código: `S = F ∩ H`, `s = |S|`, y *cuerda* = arista que
no está en `H`.

## Estructura

```
src/c/            programas exhaustivos y de búsqueda (C, sin dependencias)
src/python/       biblioteca y verificaciones (Python + networkx)
src/python/legacy/ scripts heredados de la primera fase (ver su LEEME.md)
data/             listas graph6 descargadas de House of Graphs
results/          salidas guardadas de las ejecuciones citadas en el artículo
paper/            fuentes y PDF del artículo (inglés y las dos versiones españolas)
figures/          figuras
Makefile          compila los programas en C (los de la v1 y los de src/c/v2)
```

## Instalación y uso

```bash
make                      # compila todos los programas en C
pip install -r requirements.txt
```

Los programas en C no necesitan nada más que `gcc`. Los de Python necesitan
`networkx` (los de `src/c` son los que hacen el trabajo pesado; los de Python son
la referencia independiente y las verificaciones estructurales).

`gadget.py` necesita además **nauty** (`nauty-geng`) instalado en el sistema.

## Programas en C

Todos fijan `H = (0,1,…,n−1)` y recorren 2-factores de `[n]` por retroceso sobre
máscaras de bits, con canonización por el grupo diedral donde hace falta.

| programa | qué hace | uso | resultado que sostiene |
|---|---|---|---|
| `exh` | recorre **todos** los 2-factores de `[n]` y calcula `max cor(F)` desglosado por número de ciclos de `F` | `./exh n [tope]` | la tabla exacta de `ov(n)` para `n ≤ 13`; recuentos que coinciden con A001205 |
| `exhd` | lo mismo restringido a `Γ` 4-regular (es decir `F ∩ H = ∅`) | `./exhd n [tope]` | el caso `s = 0` |
| `exhm` | variantes de modo del anterior | `./exhm n [tope] [modo]` | comprobaciones cruzadas |
| `exhs` | igual pero filtrando por `s = \|F ∩ H\|` exacto, con poda temprana | `./exhs n [tope] [s]` | la tabla del mínimo de solapamiento por `s` (la tabla en forma de V) |
| `par` | cuenta configuraciones con y sin «par paralelo limpio» | `./par n [tope]` | descartar una vía de demostración |
| `casih` | cuenta pares con `H` óptimo que tienen o no un ciclo casi-hamiltoniano | `./casih n [tope]` | descartar otra vía |
| `hunt2` | escalada 2-opt sobre `F` con reinicios, buscando `max cor` | `./hunt2 n tope semilla iters` | cotas superiores del mínimo para `n` fuera del alcance exhaustivo |
| `hunts` | la misma escalada restringida a `s ≤ smax` | `./hunts n tope semilla iters smax` | que no aparece ningún par con solapamiento `< 6` en la ventana, para `n = 14, 15` |
| `clases` | clasifica los pares extremales: cuántos hay, cuántos son unívocamente hamiltonianos y en cuántas clases diedrales caen | `./clases n obj` | `n=10`: 160/40/2 · `n=11`: 121/44/2 · `n=12`: 168/72/3 |
| `clases5` | lo mismo, mucho más rápido: si `Γ` es unívocamente hamiltoniano su único ciclo es `H`, luego el solapamiento máximo vale exactamente `s`, y un par extremal UH cumple `s = 5`; genera sólo esos | `./clases5 n` | reproduce los números de `clases` de forma independiente |
| `patron` | **búsqueda dirigida por patrón de tramos.** `S = F ∩ H` se parte en `c` caminos (*tramos*) de tamaños `k_1..k_c` con suma `s`, y entonces `n₂ = s − c` y `n₃ = 2c`. Fijado el patrón, coloca los tramos sobre `H` (uno en la arista `(0,1)`, lo que mata las rotaciones) y completa `F` **sólo con cuerdas**, porque por construcción no cabe ninguna otra arista de `H` | `./patron n` para los siete patrones, o `./patron n k1 k2 ...` para uno | reproduce la clasificación seis veces más rápido y la extiende: los únicos pares UH caen siempre en el patrón `{1,2,2}` |
| `ventana` | pregunta si existe algún par con `s ≤ smax` y solapamiento máximo `≤ 4`; enumera ciclos hamiltonianos de `Γ` con salida en cuanto uno solapa en 5 | `./ventana n smax` | `n = 13`: 415 947 992 pares examinados, 0 candidatos |

**Sobre `hunt2` y `hunts`:** son heurísticos. Dan una **cota superior** del mínimo
del solapamiento, nunca una inferior. Lo único afirmable a partir de su salida es
que no han encontrado ningún par por debajo del valor impreso.

## Biblioteca y verificaciones en Python

### Núcleo

| fichero | qué hace |
|---|---|
| `lib.py` | base: enumeración de todos los 2-factores de un grafo, recuento de ciclos |
| `maxov.py` | `ov_G(F)` por programación dinámica sobre subconjuntos — la implementación de referencia |
| `cor2.py` | `cor_G(F)` por el **criterio de ensamblaje**: `cor ≤ j` si y sólo si existe `R ⊆ F` con `\|R\| ≤ j` tal que `F∖R` es un bosque lineal generador cuyos caminos se ensamblan cíclicamente con aristas de `G` |
| `valida_cor2.py` | valida `cor2.py` contra `maxov.py` sobre casos aleatorios (1862 casos, sin discrepancias) |
| `unico.py` | cuenta ciclos hamiltonianos de `Γ = F ∪ H` por retroceso |

### Las dos familias

| fichero | qué hace |
|---|---|
| `familia.py` | genera `Γ_n`: zigzag sobre `[7,n−1]`, más el triángulo `{12,23,13}`, para todo `n ≥ 10` |
| `delta.py` | genera `Δ_n`: zigzag sobre `[8,n−1]`, más los triángulos `{12,23,13}` y `{56,67,57}` |
| `fam2.py`, `fam3.py` | las dos familias candidatas intermedias con las que se llegó a `Δ_n` |
| `forzado.py` | propagación de forzado con las reglas (R1) grado 2 fuerza ambas aristas, (R2) dos aristas forzadas saturan el vértice, (R3) una arista que une los extremos de un camino forzado con menos de `n−1` aristas queda excluida; con union-find. Cierra sobre `H` para `Γ_n` hasta `n = 60` y para `Δ_n` hasta `n = 30` |
| `ext.py`, `otros.py` | comprueban si los pares extremales coinciden arista a arista con `Γ_n` (**no lo hacen**: ese fue uno de los errores corregidos) |

### Lemas estructurales

| fichero | qué hace |
|---|---|
| `protegidas.py` | verificación exhaustiva del **lema de aristas protegidas**: si `H` es óptimo, todo ciclo hamiltoniano `H'` cumple `H∖H' ⊆ S` |
| `contrae.py` | verifica que `Γ/S` es exactamente 4-regular con `n−s` vértices, y localiza los lazos |
| `gadget.py` | busca un **bloque con puertos** (conexo, exactamente dos vértices de grado 2, el resto de grado 4, y un único camino hamiltoniano entre los dos de grado 2) sobre la salida de `nauty`. No existe ninguno de tamaño `m ≤ 13` |
| `grados_hog.py` | decodifica graph6 y calcula el perfil de grados de los grafos unívocamente hamiltonianos del catálogo de House of Graphs; `n₃` mínimo observado = 14 |

### Búsquedas dirigidas

| fichero | qué hace |
|---|---|
| `buscaUH.py` | escalada 2-opt que no deja crecer `s`, buscando uniones unívocamente hamiltonianas con `s` pequeño. Arranca en `Γ_n` |
| `annealUH.py` | la misma búsqueda, con enfriamiento simulado, que sí deja crecer `s` temporalmente |
| `cazaUH4.py` | fija `s = 4` y minimiza directamente el número de ciclos hamiltonianos de `Γ`. Llega a 2 ciclos para `n = 14` y a 4 para `n = 16, 18`, sin llegar a 1 |
| `climb.py`, `climb2.py`, `corclimb.py`, `diracclimb.py` | variantes de escalada sobre distintas funciones objetivo |
| `exceso2c.py`, `excdir.py`, `hunt.py`, `v2busca.py`, `cosbusca.py`, `dicot.py` | barridos aleatorios de condiciones locales y conjeturas intermedias |
| `exh2c.py` | búsqueda exhaustiva del máximo de `cor(F)` sobre 2-factores con exactamente `c` ciclos |

### Fase anterior (densidad topológica, orden de fusión)

`alt.py`, `alt2.py`, `beta.py` (circuitos alternantes), `bloques.py`, `chain.py`,
`chain2.py`, `conjA.py`, `conjD.py`, `dirac.py`, `dirac2.py`, `diraccut.py`,
`excescan.py`, `exceso.py`, `kstar2.py`, `local.py`, `merge3.py`, `porc.py`,
`reg4.py`, `tri.py`, `triglob.py`, `cosido.py`.

Varios de estos siguen siendo dependencias de los de arriba (`local.py`,
`cosido.py`, `merge3.py`, `maxov.py`), de modo que todo el Python vive en un único
directorio plano y los `import` funcionan sin tocar `PYTHONPATH`.

## Reproducir las tablas del artículo

```bash
make

# la función extremal exacta, n = 6..13   (n=13 tarda horas)
for n in 6 7 8 9 10 11 12 13; do ./exh $n; done

# el mínimo del solapamiento por s  (la tabla en V)
for s in 0 1 2 3 4 5 6 7 8; do ./exhs 12 7 $s; done

# clasificación por patrón de tramos (lo más rápido)
./patron 13         # los siete patrones; solo {1,2,2} da pares UH

# clasificación de los pares extremales unívocamente hamiltonianos
./clases5 10        # 40 UH, 2 clases
./clases5 11        # 44 UH, 2 clases
./clases5 12        # 72 UH, 3 clases

# verificación de la ventana s <= 4
./ventana 13 4      # 0 candidatos

# las dos familias, y el forzado que prueba su unicidad
cd src/python
python3 familia.py
python3 delta.py
python3 forzado.py 60

# el lema de aristas protegidas
python3 protegidas.py 10

# perfiles de grados del catálogo de House of Graphs
python3 grados_hog.py ../../data/hog63.g6
```

## Versión 2 (octubre 2026): gadgets, enchufes y distancia a Sheehan

Material de la §8 de la versión 2 del artículo. Todo está en `src/c/v2`,
`src/python/v2` y `results/v2`. Los programas en C se compilan con `make`.

| programa | qué hace | resultado que sostiene |
|---|---|---|
| `verif_indep` | verificador independiente escrito desde cero: recorre todos los 2-factores de `[n]`, enumera todos los ciclos hamiltonianos de `Γ` y calcula `ov(n)`, la tabla por `s`, los pares extremales y unívocamente hamiltonianos (con clases diedrales), el lema de aristas protegidas y la tabla de patrones con `s = 5` | reproduce las tablas 1–3, la clasificación y la tabla de la Obs. 5.11 para `n ≤ 12` |
| `hc` | cuenta los ciclos hamiltonianos de un grafo leído por la entrada estándar y su solapamiento máximo con un 2-factor dado | herramienta para los scripts de Python |
| `gadget` | busca todos los gadgets rígidos (camino hamiltoniano único de `w_0` a `w_{m−1}`) hasta tamaño `m`, por `s` y patrón de tramos | tabla de gadgets de la Prop. 8.3; no hay ninguno con `s = 0` ni `s = 1` |
| `gadget1` | para `s = 1`, el mayor solapamiento de los caminos interiores de cada gadget | el gadget `K₄` (`m = 4`, solapamiento 3) y la inexistencia de gadgets rígidos con `s = 1` hasta `m = 12` |
| `near11` | recorre todos los pares con patrón `{1,1}` y cuenta los ciclos que pierden una arista no compartida (el par es rígido si no hay ninguno) | ningún par rígido `{1,1}`; mínimo 3, 5, 7, 7, 7, 7, 7 para `n = 8..14` |

| script | qué comprueba |
|---|---|
| `families_check.py` | `Γ_n` y `Δ_n` construidos directamente desde las definiciones 5.1 y 5.4, para `10 ≤ n ≤ 33`, más los ejemplos de las Obs. 5.6, 5.9, 7.13 y el contraejemplo `n = 7` de la conjetura 5.8 sin la hipótesis `n ≥ 8` |
| `test_gadget.py` | lema de inserción con gadgets rígidos sobre grafos 4-regulares aleatorios |
| `test_s1.py` | lema de inserción con el gadget `K₄` (los ciclos se duplican y el solapamiento sube exactamente 3) |
| `test_double.py` | identidades de conteo de la duplicación (Lema 8.5 y los dos casos del Teorema 8.6) |
| `rigid_small.py` | todos los pares rígidos con `1 ≤ s ≤ 4` para `n ≤ 9` y su patrón (Obs. 8.8) |

```bash
make
./gadget 11 ; ./gadget1 12 ; ./verif_indep 11
CAP=40 ./near11 12
cd src/python/v2
python3 families_check.py ../../../hc
python3 test_gadget.py ../../../hc
python3 test_s1.py ../../../hc        # ejecutar desde este directorio
python3 test_double.py ../../../hc
python3 rigid_small.py ../../../hc
```

## Datos

| fichero | contenido |
|---|---|
| `data/hog_uhg.g6` | los 63 grafos unívocamente hamiltonianos con grado mínimo `≥ 3`, cintura `≥ 5` y `n ≤ 22` del catálogo de House of Graphs, más el grafo casi cúbico de Royle de orden 18 |
| `data/hog63.g6` | los mismos 63, sin el de Royle |

Fuente: <https://houseofgraphs.org/meta-directory/uniquely-hamiltonian>, listas
generadas por Goedgebeur, Meersman y Zamfirescu, *Graphs with few hamiltonian
cycles*, Math. Comp. 89 (2020) 965–991. Consultadas en octubre de 2026.

## Advertencias de honestidad

Tres cosas que conviene saber antes de fiarse de una salida:

1. `hunt2` y `hunts` son heurísticos: cota superior del mínimo, nunca inferior.
2. Los recuentos de bloques con puertos que importan son los **filtrados**
   (1, 4, 13, 50, 235, 1284, 8392, 62439 para `m = 6..13`), no los totales que
   produce el generador de `nauty` (7, 28, 124, 663, 4173, 30037, 243212, 2166792).
3. Los pares extremales **no** coinciden arista a arista con `Γ_n`; lo que es
   cierto es que `Γ_n` y `Δ_n` son las únicas clases unívocamente hamiltonianas
   para `n = 10, 11`, y que en `n = 12` aparece una tercera.
