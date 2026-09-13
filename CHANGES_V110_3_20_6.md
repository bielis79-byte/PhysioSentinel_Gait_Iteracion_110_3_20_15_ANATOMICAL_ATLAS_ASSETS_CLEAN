# CHANGES · V110.3.20.6

## Base
- Derivada directamente de V110.3.20.5 3D ESTIMATED LEFT ANKLE REFINEMENT.
- APP_VERSION actualizado a 110.3.20.6.
- Se mantiene sin cambios la arquitectura 3D estimada/no métrica y el retargeting SKEL existente.

## Mejora distal q14
- Se conserva el filtro FIR simétrico de 7 puntos y el limitador de velocidad de q14 a 3.6°/frame.
- Se añade un guard adaptativo LOCAL de curvatura temporal basado en la segunda diferencia Δ²q.
- Los umbrales se calculan de forma robusta mediante mediana + MAD de |Δ²q|, con un suelo conservador de 1.35°.
- Sólo se corrigen máximos locales de curvatura; no se suaviza globalmente toda la trayectoria.
- Cada corrección mezcla 65% de interpolación vecinal y 35% del valor ya refinado.
- Se protege >=95% del ROM posterior al guard y se mantiene el anclaje exacto del frame 1.
- q7 (tobillo derecho) y el resto de DOF no reciben este nuevo guard.

## Auditoría añadida
En `per_q` se exportan para cada DOF:
- `curvature_corrections`
- `curvature_threshold_deg`
además de rango, paso máximo, límite de velocidad y peso de filtrado ya existentes.

## Validación sobre la secuencia V110.3.20.5 aportada
Para q14 (75 frames):
- ROM: 32.247° -> 32.247° (100% retenido)
- max |Δq|: 3.600° -> 3.600°
- RMS Δq: 1.956° -> 1.868°
- max |Δ²q|: 3.485° -> 2.790°
- RMS Δ²q: 1.258° -> 1.107°
- puntos locales corregidos: 5
- corrección máxima: ~1.13°

## No modificado
- Pelvis, caderas y rodillas.
- Tronco y brazos.
- Driver distal 3D estimado.
- q7.
- Generación de `skin_verts` y jerarquía SKEL24.
- Interpretación no métrica del 3D estimado.
