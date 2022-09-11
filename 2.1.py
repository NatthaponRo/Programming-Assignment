import pandas as pd
import sqlite3

#Set variable db,con,filename,query
db = "medcury-de.db"
con = sqlite3.connect(db)
filename = 'ProductSalesAmountByMonth.csv'
query = """WITH A AS 
(SELECT *,
        LAG(SalesAmount) OVER(PARTITION BY ProductID ORDER BY Month ) AS oldsale,
        Month - LAG(Month) OVER(PARTITION BY ProductID ORDER BY Month ) AS diffmonth
   FROM(
         SELECT strftime('%Y-%m',o.OrderDate) AS yearMonth,
	        PD.ProductID,
	        PD.ProductName,
	        CAST(SUM(OD.QUANTITY * OD.UNITPRICE) AS float) AS SalesAmount,
	        O.OrderDate,
	        strftime('%m',o.Orderdate) AS Month
            FROM 'ORDER DETAILS' AS OD
                  LEFT JOIN 'ORDERS' AS O
                  ON OD.ORDERID = O.ORDERID
                  LEFT JOIN 'PRODUCTS' AS PD
                  ON OD.PRODUCTID = PD.PRODUCTID
          WHERE strftime('%Y',O.Orderdate) = '1997'
          GROUP BY yearMonth, OD.PRODUCTID)
)
SELECT yearMonth,
       ProductID,
       ProductName,
       salesAmount,
       CASE 
           WHEN diffmonth = 1 THEN ROUND((((SalesAmount/oldsale)-1) * 100),2)
           ELSE NULL 
           END AS percentage_change
   FROM A
  Order by yearMonth, ProductName
"""

#Query and set it into dataframe
df = pd.read_sql_query(query,con)

#Append Dataframe into csv file
df.to_csv(filename, mode = 'a', index = False, header=False)
con.close()