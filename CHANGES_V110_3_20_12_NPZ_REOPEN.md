# V110.3.20.12 · Reabrir NPZ SKEL

- Añade `📂 Cargar NPZ SKEL existente` al panel SKEL.
- Lee directamente vertices, faces, joints, poses/q(t), joint_names, escala y metadatos.
- Al cargar un NPZ válido, lo guarda únicamente en `st.session_state`.
- NO recalcula fitting, retargeting ni los 75 frames.
- El visor anatómico usa inmediatamente el NPZ importado.
- La pestaña `Cinemática Anatómica 3D` usa el mismo objeto importado.
- No sube el NPZ a Supabase.
- Mantiene la arquitectura Anatomical Atlas Mesh estricta: sin geometría anatómica procedural falsa.
