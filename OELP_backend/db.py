import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('site.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# # Fetch and display data from the student table
# cursor.execute('SELECT name, password FROM student')
# # conn.commit()
# students = cursor.fetchall()

# for student in students:
#     print(student)


# # Insert data into the course table
# ids=["DS3040"]
# courses=["Deep Learning"]

# for i in range(len(courses)):
# query='''INSERT INTO dailyattendance(student_mail,course_id,date,status) VALUES (?, ?,?,?);'''
# value= ("112101014","DS3040","2024-4-14",True)
# cursor.execute(query, value)
# conn.commit()


# Fetch and display data from the course table
# cursor.execute('SELECT mail FROM student')
cursor.execute('SELECT * FROM dailyattendance')
# cursor.execute('SELECT course_id, attendance_percentage FROM takes WHERE student_mail="dummy"')
# # conn.commit()
courses = cursor.fetchall()
print(courses)
for course in courses:
    print(course)

# Close the cursor and connection
cursor.close()
conn.close()


