# CHANGES · V110.3.20.7 SEGMENT + SKEL Skeleton Layer

- Rama: arquitectura segmentaria.
- Se añade capa esquelética funcional SKEL sin modificar el fitting segmentario.
- Visor: Piel / Esqueleto / Ambos.
- La capa esquelética deriva de los joints SKEL y comparte exactamente q(t) con la piel.
- Se mantiene el refinamiento temporal segmentario genérico de 7 muestras, preservación >=92% del ROM y limitador robusto bidireccional.
- q14 vuelve al peso segmentario genérico 0.62 y NO recibe el cap específico 3.6°/frame ni el guard local de curvatura de la rama 3D estimada.
- No se modifica la conectividad anatómica, pelvis, caderas, rodillas, tronco, brazos ni skinning.
- La capa ósea actual es funcional/estructural, no geometría ósea individual obtenida de TC/RM.
