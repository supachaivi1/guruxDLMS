import pandas as pd
import sqlite3

df = pd.read_excel(r'C:\Users\Bosschill\Desktop\reboot_data.xlsx')
# print(df)
database = r"C:\sqlite\db\meter.db"
conn = sqlite3.connect(database)
df.to_sql(name='reboot', con=conn, if_exists='append', index=False)
