# V110.3.20.15 · Anatomical Atlas Assets

## Objetivo
Hacer funcionales las capas Huesos reales / Músculos reales sin volver a geometrías procedurales falsas.

## BodyParts3D
- Gestor de assets anatómicos reales BodyParts3D.
- Descubre el árbol del mirror público y sus tablas FMA→nombre.
- Resuelve estructuras por nombre anatómico.
- Descarga los STL reales seleccionados.
- Caché temporal del runtime (`/tmp/physiosentinel_bodyparts3d_atlas_v2015`).
- No usa Supabase.
- No añade estas mallas al NPZ del paciente.
- Atribución CC BY-SA 2.1 Japan incluida.

## Estructuras prioritarias
Huesos:
- hemipelvis, fémur, rótula, tibia, peroné, astrágalo, calcáneo;
- húmero, radio, cúbito, escápula, clavícula.

Músculos:
- glúteo mayor/medio, iliaco, psoas mayor;
- recto femoral, vasto lateral/medial;
- bíceps femoral, semitendinoso, semimembranoso;
- gastrocnemio, sóleo, tibial anterior, fibular/peroneo largo;
- deltoides, bíceps braquial, tríceps braquial.

## Funcionamiento
1. Cargar NPZ SKEL.
2. Pulsar `Preparar atlas anatómico real BodyParts3D` la primera vez en una instancia.
3. La app descarga y cachea sólo las estructuras requeridas.
4. Las mallas se registran sobre joints/q(t) SKEL.
5. Se habilitan Huesos, Músculos y exportación MP4 por capas.

## Límite
Es un atlas anatómico de referencia registrado sobre SKEL, no una segmentación individual
del paciente por TC/RM. La morfología de los assets pertenece al atlas de referencia.
