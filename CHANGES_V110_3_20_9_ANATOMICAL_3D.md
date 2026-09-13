# V110.3.20.9 · SEGMENT GENTLE · Anatomical 3D

- Mantiene sin cambios el fitting y q(t) de V110.3.20.8.
- Esqueleto SKEL anatómico funcional v2: cadenas óseas segment-scaled y articulaciones.
- Capa muscular funcional v1: trayectos musculotendinosos visuales derivados de joints SKEL. No estima activación, fuerza ni EMG.
- Visor por capas: Piel, Esqueleto, Músculo, Piel+Esqueleto, Músculo+Esqueleto y Todo.
- NPZ añade q_names y metadatos de skeleton/muscle/kinematics versions.
- Nueva pestaña Cinemática Anatómica 3D: curvas articulares, ROM, velocidad/aceleración por frame normalizado, suavidad, simetría bilateral, coordinación, angle-angle y trayectorias relativas 3D.
- En monocular/biplanar no calibrado, profundidad/trayectorias siguen siendo estimadas/no métricas.
- No se infieren fuerzas, momentos, GRF ni activación muscular.
