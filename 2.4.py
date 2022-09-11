import pandas as pd
import sqlite3

#Set variable db,con,filename,query
db = "medcury-de.db"
con = sqlite3.connect(db)
filename = 'CategorySalesAmount-1997.csv'
query = """
SELECT strftime('%Y-%m',O.OrderDate) AS yearMonth,
       CA.CategoryID,
       CA.CategoryName,
       ROUND(SUM(OD.Unitprice*OD.Quantity),1) AS Sale
   FROM 'Order details' AS OD
        LEFT JOIN Orders AS O
        ON OD.OrderID = O.OrderID
           LEFT JOIN
              (SELECT P.ProductID,
	              P.CategoryID,
	              C.CategoryName
                 FROM Products AS P
 	  	      LEFT JOIN Categories AS C
		      ON P.CategoryID = C.CategoryID) AS CA
	    ON CA.ProductID = OD.ProductID
 WHERE yearMonth LIKE '1997%'
 GROUP BY CA.CategoryID, yearMonth
 ORDER BY yearmonth, CA.CategoryID
"""

#Query and set it into dataframe
df = pd.read_sql_query(query,con)

#Use pandas to make it pivot
df_pivot = pd.pivot_table(df, values='Sale',index=["CategoryID","CategoryName"], columns="yearMonth")
df_pivot = df_pivot.reset_index()

#Write Dataframe into csv file
df_pivot.to_csv(filename, index = False)
con.close()