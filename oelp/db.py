import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('site.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Insert dummy data into the Department table
cursor.execute("INSERT INTO department (dept_id, dept_name) VALUES (?, ?)", ('D1', 'Computer Science'))
cursor.execute("INSERT INTO department (dept_id, dept_name) VALUES (?, ?)", ('D2', 'Electrical Engineering'))

# Insert dummy data into the Course table
cursor.execute("INSERT INTO course (course_id, course_name, dept_id) VALUES (?, ?, ?)", ('C1', 'Introduction to Programming', 'D1'))
cursor.execute("INSERT INTO course (course_id, course_name, dept_id) VALUES (?, ?, ?)", ('C2', 'Database Management', 'D1'))
cursor.execute("INSERT INTO course (course_id, course_name, dept_id) VALUES (?, ?, ?)", ('C3', 'Digital Circuits', 'D2'))

# Commit the changes to the database
conn.commit()

# Fetch and display data from the student table
cursor.execute('SELECT * FROM student')
students = cursor.fetchall()

for student in students:
    print(student)

# Close the cursor and connection
cursor.close()
conn.close()
