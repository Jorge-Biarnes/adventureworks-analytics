# IMPORTAMOS LAS LIBRERÍAS NECESARIAS
import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# CONEXIÓN A LA BASE DE DATOS-
conn = pyodbc.connect(
    f"DRIVER={{SQL Server}};"
    f"SERVER={os.getenv('SERVER')};"
    f"DATABASE={os.getenv('DATABASE')};"
    f"Trusted_Connection=yes;"
)

# CONSULTA SQL PARA OBTENER LOS DATOS DE VENTAS
query = """
--------CONSULTA SQL PARA OBTENER LOS DATOS DE VENTAS DE LA BASE DE DATOS ADVENTUREWORKS--------

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

"""
# EJECUTAMOS LA CONSULTA Y CREAMOS UN DATAFRAME DE PANDAS
df = pd.read_sql(query, conn)

# CONVERTIMOS LA COLUMNA DE FECHA A FORMATO DATETIME Y EXTRAEMOS AÑO, MES Y DÍA
df['DATE'] = pd.to_datetime(df['DATE'])
df['YEAR'] = df['DATE'].dt.year
df['MONTH'] = df['DATE'].dt.month
df['DAY'] = df['DATE'].dt.day
print(df.head())

# GUARDAMOS LA QUERY EN UN ARCHIVO CSV
df.to_csv('ventas_adventure.csv', index=False)
conn.close()