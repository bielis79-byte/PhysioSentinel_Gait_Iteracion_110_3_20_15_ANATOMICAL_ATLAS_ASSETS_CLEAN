# PhysioSentinel Gait V110.3.20.6

## 3D Estimated · Adaptive Left Ankle Temporal Refinement

Esta versión parte directamente de V110.3.20.5 y mantiene su arquitectura de retargeting directo desde el 3D estimado/no métrico hacia SKEL.

### Objetivo
Reducir la brusquedad temporal residual observada en el tobillo izquierdo (`q14`) sin congelarlo, sin reducir de forma material su excursión y sin modificar el resto de la arquitectura que ya funciona.

### Cambio principal
La .20.5 limitaba q14 a 3.6°/frame. La .20.6 conserva ese mecanismo y añade un control adaptativo local de la segunda diferencia (`Δ²q`). Sólo los máximos locales de curvatura que superan un umbral robusto son corregidos mediante una mezcla conservadora con la interpolación de los frames vecinos.

### Protección de movimiento
- Se conserva el anclaje exacto del frame de referencia.
- Se protege >=95% del ROM tras la nueva corrección.
- No se aplica un segundo suavizado global.
- q7 y los restantes DOF mantienen el comportamiento de V110.3.20.5.

### Interpretación
Las coordenadas 3D estimadas siguen siendo no métricas. q7/q14 representan movimiento articular retargeteado al modelo SKEL y no deben interpretarse como medición clínica absoluta de dorsiflexión/plantarflexión.
