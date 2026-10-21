# Cambios de la versión 3 del artículo (sobre `paper/paper_en_v2.tex`)

El PDF no se ha recompilado todavía: `paper/paper_en_v2.pdf` corresponde al texto anterior.

## Resultados nuevos

- **Proposición «Port blocks, plugs and Sheehan's conjecture»** (§8.2, tras el Lema 8.5). Son equivalentes: existe un bloque con puertos (Def. 7.x), existe un enchufe (Def. 8.4) y la conjetura de Sheehan es falsa. Los enchufes son lo mismo que los gadgets rígidos con s_W = 0. Comprobado en `src/python/v3/test_cut2.py`: 400 bloques candidatos y 200 desdoblamientos de vértice.
- **Patrón {1,1,1}.** Existe un gadget con o_W = s_W = 3 desde m = 7: triángulo (0,1,6) más cuadrilátero (2,3,5,4), con dos caminos hamiltonianos. La Prop. 8.3 solo usa o_W, así que excluir los pares rígidos {1,1,1} también es tan difícil como Sheehan. Datos en `results/v3/gadgets111.txt`; inserciones comprobadas en `src/python/v3/test_gadget111.py` (300).

- **Recorrido exhaustivo de {1,1} hasta n = 15** (párrafo tras el Lema 8.9). Antes llegaba a n ≤ 14. En n = 15 hay 3 098 734 688 pares, ninguno rígido, y el mínimo de ciclos buenos pasa de 7 a 11. Para n = 13..15 ningún par tiene 8, 9 o 10 ciclos buenos. En los pares mínimos recontados, H* no está en Γ. Se añade, presentado como indicio y no como cota, que el recocido no encuentra menos de 11 para n = 16..22. Datos en `results/v3/exact11_n14_15.txt` y `results/v3/anneal11_*.txt`.

- **Definición «One-stretch plug» y Proposición «Two-edge cuts in the pattern {1,1}»** (`def:plug1`, `prop:cut11`, tras el párrafo del recorrido de {1,1}). Sea un corte de 2 aristas de Γ:
  - (a) Una sola arista del corte en S es imposible.
  - (b) Si las dos están en S, un par rígido da un bloque con puertos.
  - (c) Si un lado no tiene tramos, un par rígido da un enchufe.
  - (d) Si hay un tramo a cada lado, todo ciclo distinto de H es bueno y hay exactamente hp(X)·hp(Y) − 1 ciclos buenos.

  Suponiendo Sheehan, un par rígido {1,1} con corte existe si y solo si existe un enchufe de un tramo. No hay ninguno con ≤ 14 vértices (`plug1.c`), así que hace falta n ≥ 30. Se añade el párrafo que lo relaciona con los mínimos (3, 5, 7, 7, 7, 7, 7, 11, … y el salto de hp_min de 4 a 6 en m = 11) y con el mínimo sin cortes (7, 7, 11, 15, 15, 15, 19). Se amplía el problema abierto 4. Notas de trabajo en `CORTES-11.md`.

## Correcciones

- **Def. 8.1.** Se aclara que o_W = s_W equivale a que todo camino contenga P_W ∖ F_W. Ser rígido es una condición suficiente, no necesaria.
- **Final de §8.1, párrafo tras la Prop. 8.3 y problemas abiertos 1 y 4.** {1,1,1} deja de ser un patrón sin gadget. {1,1} es el único patrón de la ventana para el que no se sabe si es tan difícil como Sheehan (no hay gadget con o_W = s_W con m ≤ 14).
- **§8.1, gadgets rígidos con s_W = 0.** La búsqueda negativa se reinterpreta como Sheehan para órdenes pequeños.
- **§7.4 y problema abierto 2.** Encontrar un bloque con puertos refutaría Sheehan, así que la sustitución por bloques no puede cerrar el hueco del Cor. 7.x de ningún tamaño. El problema abierto 2 pasa a preguntar si (H₄) es estrictamente más fuerte que Sheehan.
- **Escalera de pesos.** Para el peso 4 (s = 2) la cota pasa de «a lo sumo 3» a «a lo sumo 2» ciclos (Lema 8.9 y Teor. 8.6).
