# PhysioSentinel Gait V110.3.20.7 SEGMENT + SKEL

Versión segmentaria destinada a comparación directa con V110.3.20.7 3D ESTIMATED.

## Capas del visor
- Piel
- Esqueleto
- Piel + Esqueleto

El esqueleto funcional se genera a partir de los mismos joints SKEL de cada frame. No recalcula ni modifica q(t).

## Tobillos
Esta rama conserva el comportamiento segmentario: q14 usa el refinamiento genérico (blend 0.62) y no incorpora el cap 3.6°/frame ni el guard de curvatura exclusivos de la rama 3D estimada.

## Objetivo
Permitir comparar con la misma representación esquelética si la arquitectura segmentaria o la 3D estimada reproduce mejor la cinemática del paciente, especialmente tibia–tobillo–pie.
