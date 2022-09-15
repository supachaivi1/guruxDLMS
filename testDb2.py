# Import module
import sqlite3

# import pandas as pd

# Connecting to sqlite
conn = sqlite3.connect('test_database.db')

# Creating a cursor object using the
# cursor() method
cursor = conn.cursor()

# Creating table
# table = """CREATE TABLE STUDENT(NAME VARCHAR(255), CLASS VARCHAR(255),
# SECTION VARCHAR(255));"""
# cursor.execute(table)
#
# # Queries to INSERT records.
# cursor.execute('''INSERT INTO STUDENT VALUES ('Raju2', '7th', 'A')''')
# cursor.execute('''INSERT INTO STUDENT VALUES ('Shyam2', '8th', 'B')''')
# cursor.execute('''INSERT INTO STUDENT VALUES ('Baburao2', '9th', 'C')''')

# Display data inserted
print("Data Inserted in the table: ")
data = cursor.execute('''SELECT NAME FROM STUDENT''')
a = list()
for row in data:
    print(row)
    a.append(row)
# Commit your changes in the database
print("data list : ", a)
conn.commit()

# Closing the connection
conn.close()
