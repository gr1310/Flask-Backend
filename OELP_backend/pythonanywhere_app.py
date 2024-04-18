from flask import Flask, jsonify, request
import sqlite3
from models import Student
# Initialize Flask app
app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('/home/oelp2024/mysite/site.db')
    # conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET'])
def server_home():
    return "Server home"

################################# LOGIN END POINTS ########################################

@app.route('/student/login', methods=['PUT'])
def student_login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Establish a connection to your database
    conn = get_db_connection()  # Replace 'your_database.db' with your actual database name

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the query to fetch the student with the given email and password
    cursor.execute("SELECT name FROM student WHERE mail=? AND password=?", (email, password))

    # Fetch the first row of the result
    student = cursor.fetchone()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    if student:
        return jsonify({"message": "Login success"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 400


@app.route('/teacher/login', methods=['PUT'])
def teacher_login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Establish a connection to your database
    conn = get_db_connection() # Replace 'your_database.db' with your actual database name

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the query to fetch the instructor with the given email and password
    cursor.execute("SELECT * FROM instructor WHERE mail=? AND password=?", (email, password))

    # Fetch the first row of the result
    instructor = cursor.fetchone()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    if instructor:
        return jsonify({"message": "Login success"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 400


################################# REGISTER END POINTS ########################################
@app.route('/student/register', methods=['POST'])
def student_registration():
    data = request.get_json()

    mail = data.get('mail')
    name = data.get('name')
    password = data.get('password')
    photo = data.get('photo')

    if not all([mail, name, password, photo]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Establish a connection to your database
    conn = get_db_connection() # Replace 'your_database.db' with your actual database name

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Check if the email already exists
    cursor.execute("SELECT * FROM student WHERE mail=?", (mail,))
    existing_student = cursor.fetchone()
    if existing_student:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
        return jsonify({'message': 'Email already exists'}), 409

    try:
        # Save image to file system or database
        # Assuming Student.save_image(mail, photo) is a method to save the image
        if Student.save_image(mail, photo):
            # Insert new student into the database
            cursor.execute("INSERT INTO students (mail, name, password, photo) VALUES (?, ?, ?, ?)",
                           (mail, name, password, photo))
            # Commit the transaction
            conn.commit()
            # Close the cursor and database connection
            cursor.close()
            conn.close()
            return jsonify({'message': 'Registration successful'}), 200
        else:
            # Close the cursor and database connection
            cursor.close()
            conn.close()
            return jsonify({'message': 'Error saving image'}), 500
    except Exception as e:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
        return jsonify({'message': str(e)}), 500



@app.route('/teacher/register', methods=['POST'])
def teacher_register():
    data = request.get_json()

    mail = data.get('mail')
    name = data.get('name')
    password = data.get('password')

    if not all([mail, name, password]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Establish a connection to your database
    conn = get_db_connection()  # Replace 'your_database.db' with your actual database name

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Check if the email already exists
    cursor.execute("SELECT * FROM instructor WHERE mail=?", (mail,))
    existing_instructor = cursor.fetchone()
    if existing_instructor:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
        return jsonify({'message': 'Email already exists'}), 409

    try:
        # Insert new instructor into the database
        cursor.execute("INSERT INTO instructor (mail, name, password) VALUES (?, ?, ?)",
                       (mail, name, password))
        # Commit the transaction
        conn.commit()
        # Close the cursor and database connection
        cursor.close()
        conn.close()
        return jsonify({'message': 'Registration successful'}), 200
    except Exception as e:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
        return jsonify({'message': str(e)}), 500

################################# FETCHING ALL EXISTING COURSES ########################################
@app.route('/student/allcourses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM course')
    courses = cursor.fetchall()

    output={"id":[],"name":[]}
    for course in courses:
        output["id"].append(course[0])
        output["name"].append(course[1])
    cursor.close()
    conn.close()

    return output, 200

################################# ADDING COURSES TO TAKES ########################################

@app.route('/<rollNumber>/add/<selectedCourse>', methods=['POST'])
def updates_takes_courses(rollNumber, selectedCourse):
    data = request.get_json()
    student_mail = data.get('mail')
    course_id = data.get('id')

    if not all([student_mail, course_id]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Establish a connection to your database
    conn = get_db_connection() # Replace 'your_database.db' with your actual database name

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    try:
        # Insert the new course into the takes table
        cursor.execute("INSERT INTO takes (student_mail, course_id, attendance_percentage) VALUES (?, ?, ?)",
                       (student_mail, course_id, 100))  # Assuming attendance percentage is set to 100 by default
        # Commit the transaction
        conn.commit()
        # Close the cursor and database connection
        cursor.close()
        conn.close()
        return jsonify({'message': 'Added successful'}), 200
    except Exception as e:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
        return jsonify({'message': str(e)}), 500


# ################################# ADDING COURSES TO TAKES ########################################

@app.route('/teacher/<rollNumber>/add/<selectedCourse>', methods=['POST'])
def updates_teaches_courses(rollNumber, selectedCourse):
    data = request.get_json()
    instructor_mail = data.get('mail')
    course_id = data.get('id')

    if not all([instructor_mail, course_id]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Establish a connection to your database
    conn = get_db_connection()  # Replace 'your_database.db' with your actual database name

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    try:
        # Insert the new course into the teaches table
        cursor.execute("INSERT INTO teaches (instructor_mail, course_id) VALUES (?, ?)",
                       (instructor_mail, course_id))
        # Commit the transaction
        conn.commit()
        # Close the cursor and database connection
        cursor.close()
        conn.close()
        return jsonify({'message': 'Added successful'}), 200
    except Exception as e:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
        return jsonify({'message': str(e)}), 500


################################# FETCHING TAKES COURSES ########################################

@app.route('/student/<rollNumber>', methods=['GET'])
def getCourses(rollNumber):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM takes')
    courses = cursor.fetchall()
    print(courses)
    output={"course_id":[],"attendance_percentage":[]}
    for course in courses:
        if(course[0]==rollNumber):
            output["course_id"].append(course[1])
            output["attendance_percentage"].append(course[2])
    for id in range(len(output["course_id"])):
        cursor.execute('SELECT * FROM course')
        courses = cursor.fetchall()
        for course in courses:
            if course[0]== output["course_id"][id]:
                output["course_id"][id]+= " "+course[1]
    print(output)
    cursor.close()
    conn.close()

    return output, 200

################################# FETCHING TEACHES COURSES ########################################

@app.route('/teacher/<rollNumber>', methods=['GET'])
def getTeacherCourses(rollNumber):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM teaches')
    courses = cursor.fetchall()
    print(courses)
    output={"course_id":[]}
    for course in courses:
        if(course[0]==rollNumber):
            output["course_id"].append(course[1])
    for id in range(len(output["course_id"])):
        cursor.execute('SELECT * FROM course')
        courses = cursor.fetchall()
        for course in courses:
            if course[0]== output["course_id"][id]:
                output["course_id"][id]+= " "+course[1]
    print(output)
    cursor.close()
    conn.close()

    return output, 200


################################# FETCHING STUDENTS ENROLLED IN PARTICULAR COURSE ########################################

@app.route('/fetch/students/<course_id>', methods=['GET'])
def getStudents(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM takes')
    courses = cursor.fetchall()
    # print(courses)

    student_mails= []
    for student in courses:
        # print(student)
        if(student[1]==course_id):
            student_mails.append((student[0],student[-1]))
    cursor.execute('SELECT * FROM student')
    infos= cursor.fetchall()
    # print(info)

    output= {"name":[],"rollno":[],"attendance":[],"photo":[]}
    for mail,att in student_mails:
        for info in infos:
            if(info[0]==mail):
                output["name"].append(info[1])
                output["rollno"].append(info[0])
                output["attendance"].append(att)
                # output["photo"].append(info[3])



    cursor.close()
    conn.close()

    return output, 200


################################# FETCHING ATTENDANCE REGUSTERY FOR TEACHER'S SIDE ########################################

@app.route('/fetch/attendance/<course_id>/<date>', methods=['GET'])
def getRecord(course_id,date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dailyattendance')
    attendance = cursor.fetchall()
    # print(courses)

    output= {"name":[], "attendance":[]}
    for data in attendance:
        print(data, date, course_id)
        if(data[2]==date and data[1]==course_id):
            output["name"].append(data[0])
            output["attendance"].append(data[-1])


    cursor.close()
    conn.close()

    return output, 200

if __name__ == '__main__':
    app.run(debug=False, port=5700)