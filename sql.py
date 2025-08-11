import sqlite3

#connect to sqlite
connection = sqlite3.connect("student.db")

#Create a cursor object to insert record, create table, retrieve

cursor = connection.cursor()

table_info = """
Create table STUDENT (NAME VARHCAR(25), CLASS VARCHAR(25),SECTION VARCHAR(25), MARKS INT);

"""

cursor.execute(table_info)


#insert some more records 

cursor.execute('''Insert Into STUDENT values('aplha','Data Science','A',70)''')
cursor.execute('''Insert Into STUDENT values('Beta','Data Science','B',90)''')
cursor.execute('''Insert Into STUDENT values('gamma','Data Science','A',76)''')
cursor.execute('''Insert Into STUDENT values('sigma','DEVOPS','A',80)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','O',95)''')

## display all the records

print("The inserted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

## Commit your changes in the database
connection.commit()
connection.close()