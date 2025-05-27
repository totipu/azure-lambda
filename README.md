# Lambda Architecture in Azure
Simulator and other artfiacts for demonstrating Lambda architecture in Azure

## Azure Resources
1. IoT Hub
2. Stream Analytics Job
3. Synapse Analytics Workspace
4. Azure Storage Account (ADLS v2 - Hierarchical Namespaces enabled)
5. Power BI Workspace (Fabric or other)

## Stream Analytics Job Query
```SQL
SELECT
    System.TIMESTAMP AS WindowsEnd, carPlate, AVG(speed) as speed, AVG(fuelConsumption) as fuelConsumption
INTO
    [power-bi]
FROM
    [tt-ecs25-iot] TIMESTAMP BY EventEnqueuedUtcTime
GROUP BY carPlate, TUMBLINGWINDOW(s, 5)

SELECT
    *
INTO
    [data-lake]
FROM
    [tt-ecs25-iot] TIMESTAMP BY EventEnqueuedUtcTime
```

## Synapse SQL

### Show the data in the data lake
```SQL
SELECT
    TOP 10 *
FROM
    OPENROWSET(
        BULK 'https://ttecs2025dl.dfs.core.windows.net/ecs2025-fs/',
        FORMAT = 'PARQUET'
    ) AS [result]
```

### Calculate today's average speed and fuel consupmtion
```SQL
SELECT
    CONVERT(DATE, EventEnqueuedUtcTime) AS actualDate, carPlate, AVG(speed) AS Speed, AVG(fuelConsumption) AS FuelConsumption
FROM
    OPENROWSET(
        BULK 'https://ttecs2025dl.dfs.core.windows.net/ecs2025-fs/',
        FORMAT = 'PARQUET'
    ) AS [result]
WHERE CONVERT(DATE, EventEnqueuedUtcTime) = CONVERT(DATE, GETDATE())
GROUP BY carPlate, CONVERT(DATE, EventEnqueuedUtcTime)
```