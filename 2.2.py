import pandas as pd
import sqlite3

#Set variable filename & read CSV
filename = 'ProductSalesAmountByMonth.csv'
df = pd.read_csv(filename)

#set variable year,month
month = ['01','02','03','04','05','06','07','08','09','10','11','12']
year = ['1996','1997']

#Use loop in year,month to filter and insert dataframe each sheet
create_xlsx = pd.ExcelWriter('ProductSalesAmount.xlsx')
with pd.ExcelWriter(create_xlsx) as writer:
    for y in year:
      for m in month:
            df_new= df[df['yearMonth'] == str(y)+'-'+str(m)]
            if df_new.empty:
                pass
            else:
                df_new.to_excel(writer, sheet_name=str(y)+'-'+str(m), index=False)  