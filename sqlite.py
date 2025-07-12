import sqlite3

## connect to SQLite
connection=sqlite3.connect('student.db')

## create a cursor to insert records,create tables etc.
cursor=connection.cursor()

## create a table
table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25));

"""
cursor.execute(table_info)

## insert records
cursor.execute('''Insert into STUDENT values('Dheeraj','B.Tech','CSE')''')
cursor.execute('''Insert into STUDENT values('Suresh','B.Tech','CSE')''')
cursor.execute('''Insert into STUDENT values('Ramesh','B.Tech','CSE')''')
cursor.execute('''Insert into STUDENT values('Naveen','B.Tech','Mechanical')''')
cursor.execute('''Insert into STUDENT values('Prem chand','M.Tech','Electrical')''')

# Display the records
print("Records in STUDENT table:")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)