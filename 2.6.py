import pandas as pd
import sqlite3

#Set variable db,con,filename,query
db = "medcury-de.db"
con = sqlite3.connect(db)
filename = 'SuppliersContact.xlsx'
query = """
SELECT *, 
       CASE 
       WHEN Fax IS NOT NULL THEN Fax
       ELSE Phone
       END AS mainContact
FROM 'Suppliers' 
"""

#Query and set it into dataframe
df = pd.read_sql_query(query, con)

#Clean by extract only number
df['mainContact'] = df['mainContact'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1)

#Write Dataframe into excel file
df.to_excel(filename, index = False)
con.close()