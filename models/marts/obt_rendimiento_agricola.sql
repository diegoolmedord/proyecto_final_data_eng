{{ config(materialized='table') }}

WITH prod AS (
    SELECT * FROM {{ ref('stg_superficie_produccion') }}
),
wdi AS (
    SELECT * FROM {{ ref('stg_wdi_paraguay') }}
)
SELECT
    -- Llave subrogada MD5 para identificar la combinación única Cultivo-Año
    MD5(CONCAT(p.cultivo, '-', p.anio)) AS id_rendimiento,
    p.cultivo,
    p.anio,
    p.superficie_ha,
    p.produccion_t,
    -- Métrica calculada derivada de rendimiento por hectárea
    CASE 
        WHEN p.superficie_ha > 0 THEN ROUND(p.produccion_t / p.superficie_ha, 2)
        ELSE 0 
    END AS rendimiento_t_ha,
    w.vab_agricultura_usd AS macro_vab_agricultura_pais
FROM prod p
LEFT JOIN wdi w 
    ON p.anio = w.anio