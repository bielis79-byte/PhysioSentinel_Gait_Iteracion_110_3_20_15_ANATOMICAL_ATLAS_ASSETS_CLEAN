# V110.3.20.11 — Anatomical Atlas Mesh

Esta versión elimina deliberadamente las geometrías procedurales (cilindros/conos/fusiformes) como sustituto de anatomía real.

## Arquitectura
- `assets/anatomical_atlas/manifest.json` define cada hueso/músculo y su registro a joints SKEL.
- Se aceptan mallas anatómicas reales OBJ o STL.
- Registro frame a frame sobre SKEL.
- No modifica fitting, q(t), joints ni la piel SKEL.
- Si faltan mallas, la app debe indicarlo; NO crea una falsa anatomía de respaldo.

## Importante
El ZIP no inventa ni redistribuye mallas anatómicas de terceros sin una licencia confirmada.
Para activar la capa anatómica real hay que colocar en `assets/anatomical_atlas/bones/` y `muscles/`
las mallas anatómicas licenciadas con los nombres del manifest.

Las mallas pueden proceder de un atlas anatómico abierto compatible, o de recursos propios.
