# results/v3 — patrones {1,1} y {1,1,1}

Generado con `src/c/v2/near11.c` (opciones nuevas `HIST`, `DETAIL`), `src/c/v3/near111.c`
(`M=2` repite {1,1}, `M=3` es {1,1,1}; opciones `HIST`, `DETAIL`, `LOC`, `CLAIMS`) y
`src/c/v3/gadget11.c`. Comprobaciones independientes en `src/python/v3`.

| fichero | qué contiene |
|---|---|
| `near11_detail_n8..13.txt` | {1,1}: histograma exacto de ciclos buenos y, para los pares con menos ciclos buenos (≤ 7 en n = 8, 9; ≤ 9 en n ≥ 10), cada ciclo bueno con las aristas perdidas por posición (`A a/la`, `B b/lb`) |
| `near11_loc_n8..14.txt` | {1,1}: `LOCHIST t` = pares cuyo ciclo bueno más cercano a H usa t cuerdas; líneas `LOC` con los pares de t ≥ 4. n = 14: 228 252 646 pares, 0 rígidos |
| `near111_n7..13.txt` | {1,1,1}: recuento, histograma, `LOCHIST`; detalle de los pares mínimos en n = 12, 13 |
| `claims11_*.txt`, `claims111_n8_12.txt` | afirmaciones C1 (hay un ciclo bueno que conserva S) y C2 (hay uno que pierde una arista contigua a un tramo); líneas `CLAIMFAIL` con los contraejemplos |
| `claims3_11_n8_12.txt`, `claims3_11_n13.txt` | {1,1}: C1, C2 y además C3 (hay un ciclo bueno que renuncia a una arista compartida), con histograma `KMASK` y líneas `C3FAIL` |
| `c3_estados_n8_12.txt`, `c3_estados_n13.txt` | {1,1}, pares donde falla C3: los 9 conteos N(s₁,s₂) por estados S/U/W de los dos tramos |
| `anneal11_n15_22.txt` | {1,1}: mejores pares del recocido simulado para n = 15..22 |
| `anneal11_n20_22_big.txt`, `anneal11_n20_22_seeded.txt` | {1,1}: segunda tanda para n = 20..22 (`CAP=3000`; más movimientos, o siembra desde n − 1) |
| `exact11_n14_15.txt` | {1,1}: histograma exacto de ciclos buenos por debajo de 12, todos los pares, n = 14 y 15 (por posición p1 del segundo tramo) |
| `det11_n13..15.txt`, `bloques11.txt`, `quot11_m5_9.txt` | {1,1}: pares con ≤ 11 ciclos buenos, su descomposición por cortes de 2 aristas y el q mínimo del cociente de la familia de dos K₄ |
| `plug1_m4_14.txt` | lados de un corte que separa los tramos («enchufes de un tramo» si hp = 1): histograma de hp por tamaño m (`src/c/v3/plug1.c`) |
| `nocut11_n8_14.txt` | {1,1}: histograma de ciclos buenos separado según Γ tenga o no un corte de 2 aristas, n = 8..14, con los pares mínimos sin corte |
| `anneal11_n20_22_best.txt` | resumen de esa tanda: líneas `SUMMARY` y pares con ≤ 15 ciclos buenos, verificados en Python |
| `gadgets11.txt` | gadgets {1,1} con o_W = s_W = 2, m ≤ 14: ninguno |
| `gadgets111.txt` | gadgets {1,1,1} con o_W = s_W = 3, m ≤ 12: existen desde m = 7, todos con dos caminos hamiltonianos |

Resumen numérico:
- {1,1}, mínimo exacto de ciclos buenos 3, 5, 7, 7, 7, 7, 7, **11** para n = 8..15; 0 rígidos hasta n = 15 (`exact11_n14_15.txt`).
- {1,1}, t mínimo máximo 3, 3, 4, 4, 4, 5, 5 para n = 8..14 (= ⌊(n+2)/3⌋).
- {1,1,1}, mínimo de ciclos buenos 3, 2, 3, 3, 3, 3, 3 para n = 7..13; 0 rígidos hasta n = 13.
- C1 se cumple en todos los pares {1,1} con n ≤ 13; falla en 1 y 3 pares {1,1,1} (n = 9, 11).

## Afirmaciones C1, C2 y C3 sobre los ciclos buenos (patrón {1,1})

Un ciclo hamiltoniano de Γ = F ∪ H es **bueno** si renuncia a alguna arista de H no compartida. Por el Cor. 7.9, un par es rígido exactamente cuando no tiene ninguno. Los tres tipos de ciclo bueno que se estudian son:

- **C1**: hay un ciclo bueno que conserva S entero.
- **C2**: hay un ciclo bueno que renuncia a una arista no compartida contigua a un tramo.
- **C3**: hay un ciclo bueno que renuncia a alguna arista compartida.

Los tres se calculan con `CLAIMS=1 near111` (función `dfsclaim()` de `src/c/v3/near111.c`, con `M=2` para {1,1}). Por cada par, `kmask` tiene el bit K encendido si algún ciclo bueno conserva exactamente el subconjunto K de S (bit i = tramo i). Las líneas `CLAIMFAIL` dan los pares donde fallan C1 o C2, y las `C3FAIL` los pares donde falla C3. Las líneas `KMASK` son el histograma de kmask, y `C3` es el resumen. Ojo: el `good=` de esas líneas está truncado en `CAP` (3 por defecto); el número real lo calcula `src/python/v3/c3_buenos.py`.

| n | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|
| pares {1,1} | 232 | 1 778 | 15 361 | 147 684 | 1 565 303 | 18 141 088 |
| falla C1 | 0 | 0 | 0 | 0 | 0 | 0 |
| falla C2 | 0 | 2 | 12 | 90 | 708 | 6 306 |
| falla C3 | 2 | 10 | 127 | 740 | 6 333 | 47 586 |

Ficheros: `claims3_11_n8_12.txt` y `claims3_11_n13.txt`. Sus líneas `CLAIMS` coinciden con `claims11_n8_12.txt` y `claims11_n13.txt`.

**Rígido ⇔ ¬C1 ∧ ¬C3.** Un ciclo bueno, o conserva S, o renuncia a alguna arista de S. Por eso un par {1,1} es rígido exactamente cuando fallan a la vez C1 y C3. Ninguna de las dos basta por separado:

- C3 es falsa: arriba está la lista de pares en los que falla.
- C1 se cumple hasta n = 13, pero demostrarla en general es tan difícil como Sheehan, por desdoblamiento de vértices (`src/python/v3/test_split.py`). Si se desdoblan dos vértices z → u–w de un grafo 4-regular G, sale un par {1,1} cuyos ciclos que contienen S corresponden a los ciclos de G compatibles en z₁ y z₂. Si G tuviera un único ciclo hamiltoniano, C1 fallaría.

Cualquier demostración de que no hay pares rígidos {1,1} tiene que combinar los dos casos. Encaja con el Lema 8.9 del paper: un par {1,1} rígido tiene como mucho los ciclos H y H*.

**La clase en la que falla C3** está formada por los pares en los que todo ciclo hamiltoniano de Γ contiene S, salvo quizá H*. Lo observado en ella:

- H* no aparece nunca (n ≤ 13).
- Todos los pares tienen un ciclo bueno local: hay una ventana de vértices consecutivos de H que se recorre por otro camino con los mismos extremos. Pero la ventana mínima crece con n (2, 2, 4, 3, 6 para n = 8..12; `src/python/v3/c3_ventana.py`), así que no hay demostración local. Es el mismo obstáculo que t = ⌊(n+2)/3⌋ en `near11_loc_*`.
- En el grafo desdoblado, la clase corresponde a desdoblamientos sin «figuras de ocho», es decir, sin ciclos de Γ que pasen por u_i y w_i sin usar la arista u_iw_i. {1,1} es tan difícil como Sheehan si y solo si existe un G 4-regular con un único ciclo hamiltoniano que admita un desdoblamiento así.

**Ley de paridad (falsa).** Para cada tramo i hay tres estados del ciclo:

- S: usa u_iw_i;
- U: contiene u_i pero no w_i;
- W: contiene w_i pero no u_i.

`c3_estados.py` cuenta N(s₁,s₂) para las 9 combinaciones y guarda los resultados en `c3_estados_n8_12.txt` y `c3_estados_n13.txt`. Hasta n = 12, en los 7 212 pares de la clase, se cumple N(S,S) ≡ N(U,S) + N(W,S) ≡ N(S,U) + N(S,W) (mod 2). En n = 13 falla en 428 de los 47 586 pares, así que **no es una ley**. Además, sin la hipótesis de la clase no hay ninguna relación lineal módulo 2 entre los 16 conteos: el rango es completo en 1 500 pares aleatorios (`c3_paridad_general.py`). Y aunque fuera cierta, no excluiría los pares rígidos: N(S,S) = 1 solo obligaría a que N(U,S) + N(W,S) fuera impar.

**Bloques con puertos.** Lo que se pide en el desdoblamiento (caminos hamiltonianos entre dos vértices de grado 2, con los demás de grado 4) es la situación de los bloques con puertos de §7. La Proposición «Port blocks, plugs and Sheehan's conjecture» (§8.2, `CAMBIOS-v3.md`) demuestra que existe un bloque con puertos ⇔ existe un enchufe ⇔ Sheehan es falso. Está comprobado en `src/python/v3/test_cut2.py`.

## Mínimo exacto en n = 14 y n = 15

`M=2 CAP=12 HIST=1 near111 n p1`, un proceso por posición p1 del segundo tramo (8 núcleos). Recorre **todos** los pares, no solo la clase en la que falla C3, y da el número exacto de pares con g < 12 ciclos buenos.

| n | pares | rígidos | g ≤ 6 | g = 7 | g = 8..10 | g = 11 | CPU |
|---|---|---|---|---|---|---|---|
| 13 | 18 141 088 | 0 | 0 | 4 | 0 | 36 | 53 s |
| 14 | 228 252 646 | 0 | 0 | 2 | 0 | 42 | 1,2 h |
| 15 | 3 098 734 688 | 0 | 0 | **0** | 0 | 40 | 7,0 h |

Comprobaciones:
- El total de n = 14 coincide con `near11_loc_n14.txt`.
- Los histogramas de p1 y n − p1 coinciden (la rotación lleva uno en el otro).
- Un par mínimo por posición (2 en n = 14, 6 en n = 15) se ha recontado en Python con `src/python/v3/verifica_anneal.py`. Los 8 recuentos coinciden.

Lo que muestra:
- **El mínimo salta de 7 a 11 en n = 15**, como anticipaba el recocido.
- Entre 7 y 11 no hay valores intermedios para n = 13..15: ningún par tiene 8, 9 o 10 ciclos buenos.
- En todos los pares mínimos comprobados, Γ tiene exactamente un ciclo hamiltoniano más que ciclos buenos: H, sin H*.
- **Corrección a lo dicho sobre el recocido:** los pares mínimos no están siempre en la clase en la que falla C3. De los 6 pares comprobados de n = 15, 3 tienen un ciclo bueno que renuncia a una arista compartida.

## Estructura de los pares mínimos: cortes de 2 aristas

Ficheros:
- `det11_n13.txt`, `det11_n14.txt`, `det11_n15.txt`: todos los pares con ≤ 11 ciclos buenos y cada ciclo bueno. Se obtienen con `M=2 DETAIL=11 near111`; en n = 14 y 15 solo se calculan las posiciones p1 ≤ n/2, porque el resto sale por rotación.
- `bloques11.txt`: el análisis de esos pares con `src/python/v3/bloques11.py`.

**Todos los pares con ≤ 11 ciclos buenos (n = 13..15) tienen un corte de 2 aristas.** Lo mismo pasa con los 110 pares del recocido con ≤ 15 (n = 15..22). Todo ciclo hamiltoniano cruza un corte {e, f} por sus dos aristas, así que atraviesa cada lado B por un camino hamiltoniano entre sus dos puertos. Si se sustituye cada lado minimal B_i por una arista, queda un cociente Q, y

  #HC(Γ) = ∏ hp(B_i) · q,  con q = número de ciclos hamiltonianos de Q que usan todas esas aristas.

Además, #HC(Γ) = g + 1 en todos los casos, porque H* nunca está. La identidad se comprueba par a par contra un recuento directo, sin ninguna excepción. Solo aparecen estos bloques:

| bloque | hp | contiene un tramo |
|---|---|---|
| K₄: camino a…a+3 de H, cuerdas a(a+2), a(a+3), (a+1)(a+3), tramo (a+1)(a+2) | 2 | sí |
| 5 vértices con un tramo | 3 | sí |
| 6 o 7 vértices con un tramo | 4 | sí |
| pentágono estrellado sobre 5 vértices consecutivos de H (K₅ menos una arista) | 6 | no |
| 6 vértices sin tramo | 8 | no |

Así se leen los mínimos:
- **7 = 2·2·2 − 1:** dos bloques K₄, uno por tramo, y un cociente con q = 2.
- **11 = 2·2·3 − 1 = 2·6·1 − 1:** o dos K₄ con q = 3, o un K₄ más un pentágono estrellado con un cociente de un solo ciclo.
- Por eso casi todos los recuentos son de la forma 4k − 1.

Con `src/c/v3/quot11.c` (`quot11_m5_9.txt`) se calcula el q mínimo de la familia de dos K₄, con un cociente de m = n − 8 vértices: 2, 2, 3, 3, 4 para m = 5..9. Eso da 7, 7, 11, 11, 15 en n = 13..17. Coincide con el exhaustivo en n = 13..15 y explica el salto a 11: con 7 vértices ningún cociente tiene solo 2 ciclos por las dos aristas.

Desde n = 17 esa familia ya no es la mejor. El 11 que encuentra el recocido en n = 16..19 y 21 es siempre un K₄ más un pentágono estrellado más un cociente de **un único** ciclo (2·6·1). Por eso no hay razón para que el mínimo siga creciendo con n. Hasta donde llegan los datos, se queda en 11.

**Consecuencia para los pares rígidos (argumento esbozado, sin redactar en detalle).** Por el Lema 8.9, un par rígido tiene #HC(Γ) ≤ 2. Supongamos que Γ tiene un corte de 2 aristas con un lado B sin tramos. H y H* recorren B por el mismo camino, el de H, porque H* contiene todas las aristas no compartidas. Entonces hp(B) = 1, y B es un enchufe: puertos de grado 3, el resto de grado 4, un único camino hamiltoniano entre los puertos. Por la Proposición sobre bloques con puertos y enchufes, eso contradice Sheehan. Así que, **suponiendo Sheehan, un par {1,1} rígido no tiene ningún corte de 2 aristas con un lado sin tramos**. Faltan dos casos: los cortes que separan los dos tramos, y los que usan una arista de S. Los pares mínimos, en cambio, siempre tienen cortes, lo que sugiere estudiar aparte los pares {1,1} sin cortes de 2 aristas.

**Actualización: el esbozo está completo en `CORTES-11.md`.** Hay cuatro casos para un corte {e, f}:
- **Exactamente una arista del corte en S:** imposible por paridad.
- **Las dos aristas en S:** un lado es un bloque con puertos, lo que contradice Sheehan.
- **Un lado sin tramos:** ese lado es un enchufe, lo que contradice Sheehan.
- **Un tramo en cada lado:** todo ciclo distinto de H es bueno, y g = hp(X)·hp(Y) − 1 exactamente.

Así que, suponiendo Sheehan, un par rígido con corte equivale a dos «enchufes de un tramo» (hp = 1). `src/c/v3/plug1.c` no encuentra ninguno con m ≤ 14 (`plug1_m4_14.txt`). La fórmula del último caso se ha comprobado en los 104 cortes de ese tipo de `det11_n13..15.txt`, y en esos pares no aparece ningún corte de los tipos imposibles.

### Mínimo exacto con corte y sin corte (n = 8..14)

Se calcula con `M=2 CAP=64 NOCUT=1 near111 n [p1]`. Es una opción nueva de `src/c/v3/near111.c`: para cada par con menos de 64 ciclos buenos, mira si Γ tiene un corte de 2 aristas. Los datos están en `nocut11_n8_14.txt`.

| n | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|
| mínimo con corte | 3 | 5 | 7 | 7 | 7 | 7 | 7 |
| **mínimo sin corte** | 7 | 7 | 11 | 15 | 15 | 15 | **19** |
| pares sin corte que lo alcanzan | 43 | 2 | 54 | 324 | 4 | 4 | 10 |

Comprobaciones:
- En n = 11, CUTHIST + NOCUTHIST reproduce el histograma completo (`HIST`).
- El test de corte se ha repetido en Python con 194 pares sin corte, entre ellos todos los mínimos de n = 13 y 14, y ninguno tiene corte.
- Los mínimos sin corte de n = 12, 13 y 14 (4 + 4 + 10 pares) se han recontado con `verifica_anneal.py`, y los recuentos coinciden.
- En n = 13 y 14, las posiciones p1 y n − p1 dan el mismo histograma.

En todos esos mínimos, #HC(Γ) = g + 1 (H* nunca está) y todos son de la clase en la que falla C3.

Lectura: los pares con pocos ciclos buenos son los que tienen un corte de 2 aristas, y su número se factoriza como en la sección anterior. Sin cortes, el mínimo crece con n: 7 → 19 entre n = 8 y n = 14, más o menos 4 cada dos o tres vértices. Si esa tendencia sigue, un par rígido {1,1} tendría que tener un corte de 2 aristas. Con el argumento esbozado arriba, suponiendo Sheehan, ese corte tendría que separar los dos tramos o usar una arista de S. Es solo una tendencia en n ≤ 14, no una cota.

## Búsqueda dirigida de pares {1,1} (`src/c/v3/anneal11.c`)

Recocido simulado con S = {01, j(j+1)} fijo. Las cuerdas de F cambian por 2-switches y la energía es log(1 + número de ciclos buenos), contados hasta `CAP=400`. Para la mejor configuración de cada reinicio, el programa da el recuento completo, `kmask` y la clase. Se usa el mismo presupuesto que en §5 del paper (40 reinicios de 25 000 movimientos). Comprobaciones:

- Calibrado contra el recorrido exhaustivo: alcanza el mínimo exacto 7 en n = 10..14.
- Sus recuentos coinciden con una enumeración independiente en Python en 15 configuraciones de n = 12.

| n | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---|---|---|---|---|---|---|---|
| reinicios (2 semillas × 40) | 80 | 80 | 80 | 80 | 80 | 80 | 80 | 80 |
| mínimo de ciclos buenos encontrado | 11 | 11 | 11 | 11 | 11 | 15 | 23 | 369 |
| reinicios cuyo mejor par falla C3 | 56 | 57 | 60 | 54 | 56 | 34 | 2 | 1 |
| reinicios que acaban en el tope `CAP` | 0 | 0 | 0 | 0 | 0 | 0 | 44 | 78 |

Con este presupuesto solo n ≤ 19 son informativos. Desde n = 20 la búsqueda se degrada: las dos semillas dan mínimos distintos (15 y 19 en n = 20, 23 y 177 en n = 21), y en n = 22 casi todos los reinicios acaban en el tope de conteo. Es el mismo fenómeno que §5 del paper describe en n = 20. Para n = 15..19 el mínimo encontrado es estable en 11: no aparece ningún par rígido ni ninguno con menos de 11 ciclos buenos. Las configuraciones con menos ciclos buenos están casi siempre en la clase en la que falla C3, así que los pares más difíciles son aquellos cuyos ciclos buenos conservan S entero. Un mínimo heurístico no es una cota: en n = 14 el valor exacto es 7, y el recocido solo lo alcanza con este presupuesto completo.

### Segunda tanda para n = 20..22: tope más alto y siembra

Se probaron dos remedios, los dos con `CAP=3000`:

- **(A) Más presupuesto:** 10 reinicios de 100 000 movimientos por n, sin siembra.
- **(B) Siembra en cadena:** opción `SEED=` de `anneal11`. Cada reinicio parte de un par de n − 1 vértices, inserta un vértice nuevo en H y desvía por él una cuerda. Se empieza en el mejor par de n = 19 (11 ciclos buenos) y el mejor par de cada n siembra el siguiente. Hay dos cadenas (semillas 31 y 32), cada una con 20 reinicios de 20 000 movimientos y `T0=0.3`.

Las salidas completas están en `anneal11_n20_22_big.txt` y `anneal11_n20_22_seeded.txt`, y el resumen con los pares de ≤ 15 ciclos buenos en `anneal11_n20_22_best.txt`. Esos 9 pares se han recontado con una enumeración independiente en Python (`src/python/v3/verifica_anneal.py`), sin ninguna discrepancia. Recuentos y clase coinciden. En los 9, Γ tiene exactamente un ciclo hamiltoniano más que ciclos buenos: H, sin H*.

Prueba de cordura de la siembra: desde el par de 7 ciclos buenos de n = 14, la siembra a n = 15 vuelve a dar 11.

| n | 20 | 21 | 22 |
|---|---|---|---|
| primera tanda (`CAP=400`) | 15 | 23 | 369 |
| (A) 10 × 100 000 | 23 | **11** | 15 |
| (B) cadena semilla 31 | 15 | **11** | 19 |
| (B) cadena semilla 32 | 15 | 19 | 15 |
| **mínimo encontrado** | **15** | **11** | **15** |
| reinicios que acaban en el tope | 0 | 0 | 0 |

Ningún reinicio de esta tanda acaba en el tope, así que el problema de conteo de la primera tanda desaparece con `CAP=3000`. El valor 369 de n = 22 era un artefacto del tope.

En n = 21 se vuelve a encontrar el valor 11 por dos caminos independientes: el recocido sin siembra (j = 5) y la cadena 31 (j = 14). En n = 20 y n = 22 el mínimo es 15 en tres búsquedas distintas. No aparece ningún par rígido. Todos los pares con ≤ 15 ciclos buenos están en la clase en la que falla C3. Los primeros fuera de ella tienen 17 (n = 20 y n = 21, kmask = 10). Que n = 20 y n = 22 se queden en 15 mientras n = 21 baja a 11 puede ser falta de búsqueda o un efecto real de paridad de n; con estos datos no se puede distinguir.
