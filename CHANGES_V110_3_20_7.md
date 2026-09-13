# PhysioSentinel Gait V110.3.20.7 — 3D ESTIMATED · SKEL Skeleton Layer

Base: V110.3.20.6 3D ESTIMATED ADAPTIVE LEFT ANKLE.

## Cambio principal
- Añade una capa esquelética funcional derivada directamente de los joints y cadenas cinemáticas SKEL.
- El visor SKEL incorpora tres modos: Piel / Esqueleto / Ambos.
- La capa esquelética usa la misma secuencia q(t), joints, transformación y temporización que la piel SKEL.

## Preservado sin cambios
- Fitting SKEL y arquitectura 3D estimada.
- q(t), incluyendo q7 y q14.
- Refinamiento temporal adaptativo del tobillo izquierdo de V110.3.20.6.
- 6890 vértices de la malla cutánea por frame.
- Coordenadas científicas del NPZ; el centrado/orientación del visor sigue siendo sólo visual.

## Trazabilidad
El NPZ exportado añade:
- `skeleton_layer_version = functional_skel_v1`
- `skeleton_layer_semantics`

## Alcance
Esta versión representa un esqueleto funcional de articulaciones/cadenas SKEL. No es todavía una malla ósea individual procedente de TC/RM ni debe interpretarse como anatomía ósea interna específica del paciente.
