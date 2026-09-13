# V110.3.20.14 · NPZ Standalone Mode

## Problema corregido
En V110.3.20.13 era posible cargar un NPZ, pero parte de la interfaz seguía asumiendo que
los resultados frontal/lateral ya se habían calculado en la sesión actual.

## Nuevo modo NPZ autónomo
- El NPZ puede cargarse al entrar en SKEL, antes de volver a procesar vídeos.
- Reconstruye directamente:
  - piel/malla SKEL;
  - 75 frames ya guardados;
  - q(t) y joints;
  - curvas de cadera, rodilla, tobillo, tronco, hombro y codo;
  - ROM;
  - velocidad/aceleración normalizadas por frame;
  - simetría angular;
  - coordinación intersegmentaria;
  - trayectorias relativas 3D;
  - atlas anatómico si las mallas reales están instaladas;
  - vídeos offline por capas si las mallas correspondientes existen.
- No repite fitting, retargeting ni generación de 75 frames.

## Límite importante
Un NPZ SKEL antiguo NO contiene necesariamente todas las métricas 2D específicas de
los vídeos frontal y lateral. Esas métricas sólo pueden reaparecer sin vídeo si se
guardan también dentro del registro/Clinical Lite en una versión posterior.
