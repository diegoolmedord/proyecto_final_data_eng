WITH unpivoted AS (
    SELECT cultivo, 2018 AS anio, superficie_2017_2018_ha AS superficie_ha, produccion_2017_2018_t AS produccion_t FROM {{ source('main', 'superficie_produccion_raw') }}
    UNION ALL
    SELECT cultivo, 2019 AS anio, superficie_2018_2019_ha AS superficie_ha, produccion_2018_2019_t AS produccion_t FROM {{ source('main', 'superficie_produccion_raw') }}
    UNION ALL
    SELECT cultivo, 2020 AS anio, superficie_2019_2020_ha AS superficie_ha, produccion_2019_2020_t AS produccion_t FROM {{ source('main', 'superficie_produccion_raw') }}
    UNION ALL
    SELECT cultivo, 2021 AS anio, superficie_2020_2021_ha AS superficie_ha, produccion_2020_2021_t AS produccion_t FROM {{ source('main', 'superficie_produccion_raw') }}
)
SELECT 
    TRIM(cultivo) AS cultivo,
    CAST(anio AS INTEGER) AS anio,
    CAST(superficie_ha AS INTEGER) AS superficie_ha,
    CAST(produccion_t AS INTEGER) AS produccion_t
FROM unpivoted