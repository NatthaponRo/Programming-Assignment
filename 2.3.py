import pandas as pd
import sqlite3

#Set variable db,con,filename,query
db = "medcury-de.db"
con = sqlite3.connect(db)
filename = 'SupplierShipDuration-1997.csv'
query = """
SELECT supplierID,
       Shipcountry, 
       ROUND(AVG(JULIANDAY(Shippeddate)-JULIANDAY(Orderdate)),2) as "duration(day)"
   FROM 'Order details' AS OD
      LEFT JOIN 'Orders' AS O
      ON OD.OrderID = O.OrderID
      LEFT JOIN 'Products' AS P
      ON OD.ProductID = P.ProductID
 WHERE Orderdate LIKE '1997%'
 Group by shipCountry, SupplierID
 Order by "duration(day)" DESC, supplierID
"""
#Query and set it into dataframe
df = pd.read_sql_query(query,con)

#Write Dataframe into csv file
df.to_csv(filename, index = False)
con.close()