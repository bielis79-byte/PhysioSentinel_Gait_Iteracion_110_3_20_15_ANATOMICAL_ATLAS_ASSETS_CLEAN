-- PhysioSentinel Gait V95
-- Solo añade METADATOS sobre la versión del atlas anatómico.
-- NO almacena Z-Anatomy.zip, Z-Biomechanics.7z ni ningún binario en Supabase.

alter table public.gait_sessions
    add column if not exists atlas_version text;

comment on column public.gait_sessions.atlas_version is
    'Identificador ligero del atlas anatómico usado por PhysioSentinel; p.ej. ZAnatomy_Gait_v1. Los binarios permanecen fuera de Supabase.';
