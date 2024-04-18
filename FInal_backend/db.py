import sqlite3
from models import ImageRotator
from datetime import date
# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('site.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the image_rotator table if it doesn't exist
# cursor.execute('''CREATE TABLE IF NOT EXISTS image_rotator (
#                 course_id TEXT PRIMARY KEY,
#                 course_name TEXT,
#                 image_data TEXT,
#                 date DATE)''')

# Insert data into the image_rotator table
cursor.execute("INSERT INTO image_rotator (course_id, course_name, image_data, date) VALUES (?, ?, ?, ?)",
               ('1234', 'Computer Science', 'a43s5d6 f7g87nhm98ek90wkv98bretr66qw98', '2024-03-04'))

# Commit the changes to the database
conn.commit()

# Fetch and display data from the image_rotator table
cursor.execute('SELECT * FROM image_rotator')
image_rotators = cursor.fetchall()

for image_rotator in image_rotators:
    print(image_rotator)

# Close the cursor and connection
cursor.close()
conn.close()
