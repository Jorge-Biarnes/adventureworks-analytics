--------CONSULTA SQL PARA OBTENER LOS DATOS DE VENTAS DE LA BASE DE DATOS ADVENTUREWORKS--------
-- prueba de cambios
/*
REFERENCIA DE LAS TABLAS UTILIZADAS:
DD = DimDate
FIS = FactInternetSales
DC = DimCustomer
DP = DimProduct
DPC = DimProductCategory
DG = DimGeography
*/

SELECT
	DD.[FullDateAlternateKey] AS DATE,
	FIS.[SalesOrderNumber] AS ORDER_NUMBER,
    FIS.[SalesAmount] AS SALES_AMOUNT,
	DC.[FirstName] AS NAME,
	DC.[LastName] AS LAST_NAME,
	DP.[EnglishProductName] AS PRODUCT_NAME,
	DPC.[EnglishProductCategoryName] AS PRODUCT_CATEGORY_NAME,
	DG.[City],
	DG.[EnglishCountryRegionName] AS COUNTRY

-- JOIN DE LAS TABLAS PARA OBTENER LOS DATOS NECESARIOS
FROM [AdventureWorksDW2022].[dbo].[FactInternetSales] FIS
INNER JOIN [AdventureWorksDW2022].[dbo].[DimDate] DD
ON  DD.[DateKey] = FIS.[OrderDateKey]

INNER JOIN [AdventureWorksDW2022].[dbo].[DimCustomer] DC
ON DC.[CustomerKey] = FIS.[CustomerKey]

INNER JOIN [AdventureWorksDW2022].[dbo].[DimProduct] DP
ON DP.[ProductKey] = FIS.[ProductKey]

INNER JOIN [AdventureWorksDW2022].[dbo].[DimProductSubcategory] DPS
ON DPS.[ProductSubcategoryKey] = DP.[ProductSubcategoryKey]

INNER JOIN [AdventureWorksDW2022].[dbo].[DimProductCategory] DPC
ON DPC.[ProductCategoryKey] = DPS.[ProductCategoryKey]

INNER JOIN [AdventureWorksDW2022].[dbo].[DimGeography] DG
ON DG.[GeographyKey] = DC.[GeographyKey]

-- ORDENAMOS LOS RESULTADOS POR FECHA DE MANERA DESCENDENTE
ORDER BY DD.[FullDateAlternateKey] DESC