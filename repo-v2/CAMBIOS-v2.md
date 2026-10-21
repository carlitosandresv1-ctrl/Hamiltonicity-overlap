# Cambios de la versión 2 del artículo

## Resultados nuevos (§8 «Gadgets, plugs, and the distance to Sheehan's conjecture»)

- **Lema 8.2 (inserción) y Proposición 8.3.** Para cada k = 0, 1, 2, 3, 4, que todos los pares con |F ∩ H| = k cumplan ov ≥ 5 ya implica la conjetura de Sheehan. Ninguna franja de la ventana s ≤ 4 es más fácil que Sheehan; para k = 4 tampoco lo es ningún patrón de tramos. La Obs. 9.2, antes heurística, queda demostrada.
- **Lema 8.5 (duplicación) y Teorema 8.6.** Un par rígido cuyas aristas compartidas forman un solo camino da un grafo 4-regular simple con un único ciclo hamiltoniano.
- **Corolario 8.7.** Sheehan ⇔ ov(n) ≥ 1 para todo n ⇔ ov(n) ≥ 2 para todo n.
- **Obs. 8.8.** Los únicos pares rígidos con 1 ≤ s ≤ 4 y n ≤ 9 tienen al menos dos tramos. Ninguna construcción uniforme puede servir para todos los órdenes.
- **Lema 8.9.** Estructura de los pares rígidos con patrón {1,1}: como mucho dos ciclos hamiltonianos, H y H*, y H* existe solo si F contiene un cuadrilátero concreto. Incluye el recorrido exhaustivo del patrón {1,1} hasta n = 14: ningún par rígido.
- Escalera de pesos actualizada y un problema abierto nuevo: la equivalencia con Sheehan.

## Correcciones

- **Conjetura 5.8.** Se añade la hipótesis n ≥ 8, con el contraejemplo explícito en n = 7 (triángulo + cuadrilátero, patrón {2,3}).
- **Resumen.** Lo que fija el perfil de grados es el número de tramos, no el patrón {1,2,2}.
- **«Composición» → «partición»** de 5, en cuatro sitios.
- **Demostración del Teorema 5.3 (cremallera).** Las cuerdas hacia vértices interiores del arco se excluyen por (R2), no por (R3).
- **Obs. 5.12 y 10.3.** El Lema 7.5 no obliga al segundo ciclo a perder una arista no compartida. El texto ahora distingue los dos casos (solapamiento exactamente s, o al menos s + 1).
- Autor y agradecimientos sincronizados con el PDF publicado en GitHub. El `.tex` del archivo anterior era una versión previa.

## Repositorio

- El código está descomprimido; antes solo había `repo-final.tar.gz`.
- Programas nuevos en `src/c/v2`, scripts en `src/python/v2` y salidas en `results/v2` (ver la sección «Versión 2» del README).
- `src/barrido.sh` y `src/trozos.sh` ya no dependen de la ruta `/home/claude/work`.
- El `Makefile` compila también los programas nuevos.
