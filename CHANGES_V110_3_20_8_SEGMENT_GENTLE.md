# CHANGES · V110.3.20.8 SEGMENT + SKEL · estabilización suave q14

Base: V110.3.20.7 SEGMENT + SKEL Skeleton Layer.

## Cambio principal
- Se mantiene intacta la arquitectura segmentaria y la capa esquelética SKEL.
- Se añade una estabilización local muy suave y exclusiva de `q14` (tobillo izquierdo).
- Detección: curvatura temporal local `Δ²q14` con umbral robusto y suelo de 4.2°.
- Corrección: sólo 25% hacia la interpolación de los frames vecinos.
- Preservación de al menos 99% del ROM de la trayectoria segmentaria refinada.
- Frame 1 permanece anclado exactamente.

## Lo que NO se aplica
- No se impone cap de 3.6°/frame.
- No se copia el guard de curvatura fuerte de la rama 3D ESTIMATED.
- No se suavizan vértices ni joints directamente: se modifica q14 y luego se recalcula `SKEL.forward()`.
- `q7` y el resto de DOF mantienen el refinamiento segmentario previo.

## Objetivo
Reducir picos aislados de brusquedad del tobillo izquierdo sin perder la apariencia segmentaria más natural observada visualmente.
