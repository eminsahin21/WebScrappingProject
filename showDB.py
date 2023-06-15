import sqlite3

connection = sqlite3.connect("DENEME.db")
cursor = connection.cursor()

id = 17

cursor.execute("""SELECT pc_id,marka,fiyat,puan FROM bilgisayar WHERE pc_id={}""".format(id))

student_info = cursor.fetchall()
for student in student_info:
    print(student)

connection.commit()
connection.close()