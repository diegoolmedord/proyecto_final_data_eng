SELECT 
    CAST(anio AS INTEGER) AS anio,
    CAST(vab_agricultura_usd AS DOUBLE) AS vab_agricultura_usd
FROM {{ source('main', 'wdi_paraguay_raw') }}