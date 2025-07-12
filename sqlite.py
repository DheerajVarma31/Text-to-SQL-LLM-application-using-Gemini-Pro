import sqlite3

# ✅ Connect to SQLite (creates the DB if it doesn't exist)
connection = sqlite3.connect('student.db')

# ✅ Create a cursor for executing SQL commands
cursor = connection.cursor()

# ✅ Drop the table if it already exists (optional reset)
cursor.execute("DROP TABLE IF EXISTS STUDENT")

# ✅ Create the STUDENT table
table_info = """
CREATE TABLE STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25)
);
"""
cursor.execute(table_info)

# ✅ Insert student records
students = [
    ('Dheeraj', 'B.Tech', 'CSE'),
    ('Suresh', 'B.Tech', 'CSE'),
    ('Ramesh', 'B.Tech', 'CSE'),
    ('Naveen', 'B.Tech', 'Mechanical'),
    ('Prem chand', 'M.Tech', 'Electrical')
]

cursor.executemany("INSERT INTO STUDENT (NAME, CLASS, SECTION) VALUES (?, ?, ?)", students)
connection.commit()

# ✅ Display inserted records
print("📄 Records in STUDENT table:")
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

# ✅ Close the connection
connection.close()
