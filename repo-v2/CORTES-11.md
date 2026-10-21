# Pares {1,1} con un corte de 2 aristas

Nota de trabajo (v3). No está en el paper. Notación del paper:
- (F, H) es un par, Γ = F ∪ H y S = F ∩ H = {u₁w₁, u₂w₂}, dos tramos unitarios disjuntos.
- H = u₁w₁ A u₂w₂ B u₁.
- Los vértices u_i, w_i tienen grado 3 en Γ y todos los demás grado 4.
- Un ciclo hamiltoniano de Γ es **bueno** si renuncia a alguna arista no compartida de H. Por el Cor. 7.9 (`cor:reform`), el par es rígido si y solo si Γ no tiene ciclos buenos.
- Para un lado X de un corte, hp(X) es el número de caminos hamiltonianos de Γ[X] entre sus dos puertos.

## Resultado

**Teorema.** Sea (F, H) un par {1,1} cuyo Γ tiene un corte de 2 aristas {e, f}. Entonces e, f ∈ H, y los lados X e Y del corte son los conjuntos de vértices de los dos arcos de H − {e, f}. Además:

- (a) No puede pasar que exactamente una de e, f esté en S.
- (b) Si e, f ∈ S y el par es rígido, el lado X = A es un bloque con puertos (Def. `def:gadget`), y la conjetura de Sheehan es falsa.
- (c) Si e, f ∉ S, uno de los lados no contiene ningún tramo y el par es rígido, ese lado es un enchufe (Def. `def:plug`), y la conjetura de Sheehan es falsa.
- (d) Si e, f ∉ S y cada lado contiene un tramo, entonces **todo ciclo hamiltoniano distinto de H es bueno**, y Γ tiene exactamente hp(X)·hp(Y) − 1 ciclos buenos. En particular, el par es rígido si y solo si hp(X) = hp(Y) = 1.

**Corolario.** Si la conjetura de Sheehan es cierta, un par {1,1} rígido con un corte de 2 aristas está en el caso (d) y sus dos lados son *enchufes de un tramo*. Recíprocamente, sin suponer nada, dos enchufes de un tramo pegados por un corte de 2 aristas forman un par {1,1} rígido. Por tanto, suponiendo Sheehan:

> existe un par {1,1} rígido con un corte de 2 aristas ⇔ existe un enchufe de un tramo.

**Definición (enchufe de un tramo).** Es un grafo simple X con estas propiedades:
- tiene un camino hamiltoniano P de x a y y una arista s = ab de P;
- (E(X) ∖ E(P)) ∪ {s} es un 2-factor de X;
- P es el **único** camino hamiltoniano de X de x a y.

Entonces x, y, a y b tienen grado 3, o grado 2 cuando x o y es un extremo de s, y los demás vértices tienen grado 4. Son exactamente los lados del caso (d) con hp = 1.

## Demostración

**Lema 1 (el corte).** H es un ciclo que pasa por los dos lados, así que cruza el corte un número par de veces, al menos 2, y solo puede hacerlo por e y por f. Por tanto e, f ∈ H, y X e Y son los dos arcos de H − {e, f}. Lo mismo vale para cualquier ciclo hamiltoniano C: contiene e y f, y recorre X por un camino hamiltoniano de Γ[X] entre los extremos x (de e) e y (de f) que están en X. Recíprocamente, dos caminos así, uno en X y otro en Y, junto con e y f, forman un ciclo hamiltoniano. Así que #HC(Γ) = hp(X)·hp(Y). Además x ≠ y: si fueran iguales, X = {x}, y x tendría grado ≤ 2. Las aristas de F que no son e ni f no cruzan el corte. Escribimos P_X = H ∩ Γ[X], que es un camino hamiltoniano de x a y.

**Lema 2 (un lado con a lo sumo una arista de S).** Supongamos que P_X contiene a lo sumo una arista de S, y sea Q ≠ P_X otro camino hamiltoniano de Γ[X] de x a y. Entonces el ciclo C = Q ∪ P_Y ∪ {e, f} es bueno.

*Demostración.* C es un ciclo hamiltoniano distinto de H, y H ∖ C = P_X ∖ Q. Como |Q| = |P_X| y Q ≠ P_X, ese conjunto no es vacío. Si C no fuera bueno, H ∖ C ⊆ S, y entonces P_X ∖ Q = {s} para la única arista s = ab de S en P_X. En ese caso Q contiene P_X − s, que son dos caminos: uno de x a a y otro de b a y (o con a y b intercambiados). Esos dos caminos cubren X, y la única arista de Γ que los une en un camino de x a y es ab = s, porque Γ es simple. Eso contradice s ∉ Q. ∎

En particular, si el par es rígido y P_X contiene a lo sumo una arista de S, entonces hp(X) = 1.

**(a)** Si e = u₁w₁ ∈ S y f ∉ S, entonces u₁ está en X y w₁ en Y, y u₂, w₂ están en el mismo lado. La suma de los grados en Γ de los vértices de X es 4|X| − 1 − (0 o 2), que es impar. Pero también vale 2|E(Γ[X])| + 2, que es par. Contradicción. Este caso no usa la rigidez.

**(b)** e = u₁w₁ y f = u₂w₂, de modo que X = {w₁, …, u₂} (el arco A) no contiene ninguna arista de S. Por el Lema 2, hp(X) = 1. En Γ[X], w₁ y u₂ tienen grado 2 y los demás grado 4. Γ[X] es conexo, porque tiene un camino hamiltoniano. Es por tanto un bloque con puertos, y por la Prop. `prop:portplug` Sheehan es falsa.

**(c)** Si X no contiene ningún tramo, todos sus vértices tienen grado 4 en Γ. En Γ[X], los puertos x ≠ y tienen grado 3 y los demás grado 4, y Γ[X] es simple. Por el Lema 2, hp(X) = 1, así que Γ[X] es un enchufe y Sheehan es falsa (Lema `lem:doubling`).

**(d)** Cada lado contiene exactamente una arista de S. Sea C ≠ H un ciclo hamiltoniano. Por el Lema 1, C = Q_X ∪ Q_Y ∪ {e, f}, con Q_X ≠ P_X o Q_Y ≠ P_Y; digamos Q_X ≠ P_X. Si C no fuera bueno, P_X ∖ Q_X ⊆ S, y el argumento del Lema 2 da una contradicción. Por tanto todo ciclo hamiltoniano distinto de H es bueno (en particular H* no está en Γ), y el número de ciclos buenos es hp(X)·hp(Y) − 1. ∎

*Pegado.* Si X e Y son enchufes de un tramo, se unen el puerto y_X con x_Y y el puerto y_Y con x_X por aristas nuevas, que se añaden a H. Sale un par {1,1}:
- H es P_X, la arista y_X x_Y, P_Y y la arista y_Y x_X;
- F es la unión de los 2-factores de X y de Y;
- F ∩ H es el conjunto de los dos tramos, que son unitarios y están en lados distintos;
- su único ciclo hamiltoniano es H, por el Lema 1.

## Comprobación por ordenador

Programa `src/c/v3/plug1.c`. Para cada tamaño m enumera todos los lados posibles del caso (d): P = 0…m−1, tramo en jj+1 con j ≤ (m−2)/2 (el resto sale por reflexión), y todos los 2-factores F_X con F_X ∩ P = {jj+1}. Para cada uno cuenta hp. Resultados en `results/v3/plug1_m4_14.txt`.

| m | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| lados | 1 | 1 | 11 | 59 | 533 | 3 969 | 42 617 | 404 132 | 5 115 578 | 58 790 997 | 859 523 728 |
| hp mínimo | 2 | 3 | 4 | 4 | 4 | 4 | 4 | 6 | 6 | 6 | 6 |
| enchufes de un tramo (hp = 1) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Una primera versión de `plug1.c` generaba algunos 2-factores varias veces. Eso infló el recuento de lados, pero no el mínimo de hp ni la ausencia de enchufes, porque todos los lados se visitaban. Está corregido, y el recuento corregido coincide con una enumeración por fuerza bruta en Python para m = 6..8.

Hay valores de hp impares (3, 5, 7, 9, 11…), así que no hay ninguna obstrucción de paridad.

Comprobaciones independientes (`src/python/v3/test_plug1.py`):
- Una enumeración en Python, comprobada contra fuerza bruta sobre todos los conjuntos de cuerdas, reproduce los histogramas de m = 6, 7, 8.
- 300 pares obtenidos pegando dos lados al azar son pares {1,1} válidos y tienen exactamente hp(X)·hp(Y) ciclos hamiltonianos.

**Consecuencia numérica.** Por (d), el mínimo de ciclos buenos entre los pares {1,1} de n vértices con un corte que separa los tramos es

  min { hp_min(a)·hp_min(b) : a + b = n, a, b ≥ 4 } − 1,

que vale 3, 5, 7, 7, 7, 7, 7, 11, 11, 11, 11 para n = 8..18. Coincide con los mínimos exactos de `nocut11_n8_14.txt` (pares con corte) y de `exact11_n14_15.txt` (n = 15). El salto de 7 a 11 en n = 15 es el salto de hp_min de 4 a 6 en m = 11. Los bloques que aparecían en `bloques11.txt` son los lados de mínimo hp: el K₄ (m = 4, hp = 2), el de 5 vértices (hp = 3) y los de 6 y 7 (hp = 4).

**Consecuencia para los pares rígidos.** Suponiendo Sheehan, un par {1,1} rígido con un corte de 2 aristas necesita dos enchufes de un tramo, y por la tabla cada uno tiene m ≥ 15. Así que tendría n ≥ 30.

## Lo que queda abierto

- **Existencia de enchufes de un tramo.** No se sabe si su existencia equivale a refutar Sheehan. Pegar un enchufe de un tramo consigo mismo da un par {1,1} rígido con un único ciclo hamiltoniano, pero con cuatro vértices de grado 3, no 4-regular. Contraer el tramo da un grafo con solo dos vértices de grado 3, pero puede crear caminos «incompatibles», que es el mismo obstáculo de la Observación `rem:ports`.
- **Pares sin cortes de 2 aristas.** Ahí el mínimo de ciclos buenos crece: 7, 7, 11, 15, 15, 15, 19 para n = 8..14 (`nocut11_n8_14.txt`). Es solo una tendencia.
