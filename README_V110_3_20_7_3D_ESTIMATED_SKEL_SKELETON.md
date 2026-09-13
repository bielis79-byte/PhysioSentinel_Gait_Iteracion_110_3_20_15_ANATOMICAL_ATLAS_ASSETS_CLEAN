# V110.3.20.7 — 3D ESTIMATED + SKEL Skeleton Layer

Primera versión de la arquitectura visual multicapa del módulo SKEL.

Capas disponibles en el visor:
1. Piel SKEL.
2. Esqueleto funcional SKEL.
3. Piel + esqueleto.

El esqueleto no recalcula el movimiento: se deriva de los joints SKEL ya resueltos frame a frame. Por ello no modifica el fitting ni las trayectorias articulares de V110.3.20.6.

Siguiente evolución prevista: sustituir progresivamente la representación funcional por geometrías óseas anatómicas registradas al esqueleto SKEL y, después, añadir la tercera capa muscular.
