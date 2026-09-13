# V110.3.20.13 · Anatomical Atlas + Offline Video Export

## Correcciones
- Los botones Huesos/Músculos del visor ya NO dejan la escena en blanco cuando no hay atlas real:
  quedan desactivados si no existen mallas anatómicas reales.
- La piel sigue disponible desde el NPZ SKEL.

## Vídeo
Se añade exportación OFFLINE completa desde los frames ya calculados:
- 🎬 Piel
- 🎬 Huesos
- 🎬 Músculos
- 🎬 Todas las capas

El exportador:
- recorre los 75 frames en servidor;
- no usa captura en tiempo real del navegador;
- no vuelve a ejecutar fitting ni retargeting;
- produce MP4 H.264 descargable;
- utiliza cámara y límites fijos para evitar bombeo/zoom entre frames.

## Atlas
- Continúa el modo STRICT_REAL_MESH.
- Sin cilindros/conos/fusiformes como sustitutos anatómicos.
- Huesos/Músculos sólo se habilitan cuando hay OBJ/STL reales en `assets/anatomical_atlas`.
