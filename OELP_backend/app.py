from flask import Flask, request, jsonify
from models import *
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

################################# HOME ########################################
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

    student = Student.query.filter_by(mail=email, password=password).first()
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

    instructor = Instructor.query.filter_by(mail=email, password=password).first()
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

    if Student.query.filter_by(mail=mail).first():
        return jsonify({'message': 'Email already exists'}), 409

    if Student.save_image(mail, photo):
        new_student = Student(mail=mail, name=name, password=password, photo=photo)
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Registration successful'}), 200
    else:
        return jsonify({'message': 'Error saving image'}), 500

@app.route('/teacher/register', methods=['POST'])
def teacher_register():
    data = request.get_json()

    mail = data.get('mail')
    name = data.get('name')
    password = data.get('password')

    if not all([mail, name, password]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if Instructor.query.filter_by(mail=mail).first():
        return jsonify({'message': 'Email already exists'}), 409
    
    new_instructor = Instructor(mail=mail, name=name, password=password)
    db.session.add(new_instructor)
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 200

################################# FETCHING ALL EXISTING COURSES ########################################
@app.route('/student/allcourses', methods=['GET'])
def get_courses():
    conn = sqlite3.connect('site.db')
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
def updates_takes_courses(rollNumber,selectedCourse):
    data= request.get_json()
    student_mail= data.get('mail')
    course_id= data.get('id')
    # if not course_id:
    #     return jsonify({'message': "'None' courses can't be added"}), 400
    
    # if Takes.query.filter_by(student_mail=student_mail).first():
    #     return jsonify({'message': 'Email already exists'}), 409
    
    new_course = Takes(student_mail=student_mail, course_id=course_id, attendance_percentage=100)
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Added successful'}), 200

################################# ADDING COURSES TO TAKES ########################################

@app.route('/teacher/<rollNumber>/add/<selectedCourse>', methods=['POST'])
def updates_teaches_courses(rollNumber,selectedCourse):
    data= request.get_json()
    instructor_mail= data.get('mail')
    course_id= data.get('id')
    # if not course_id:
    #     return jsonify({'message': "'None' courses can't be added"}), 400
    
    # if Takes.query.filter_by(student_mail=student_mail).first():
    #     return jsonify({'message': 'Email already exists'}), 409
    
    new_course = Teaches(instructor_mail=instructor_mail, course_id=course_id)
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Added successful'}), 200

################################# FETCHING TAKES COURSES ########################################

@app.route('/student/<rollNumber>', methods=['GET'])
def getCourses(rollNumber):
    conn = sqlite3.connect('site.db')
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
    conn = sqlite3.connect('site.db')
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
    conn = sqlite3.connect('site.db')
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
    conn = sqlite3.connect('site.db')
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

################################# UPDATING ATTENDANCE REGISTERY FROM TEACHER'S SIDE ########################################

@app.route('/update/attendance/<student_mail>/<date>/<course_id>', methods=['PUT'])
def updateRecord(student_mail,date,course_id):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dailyattendance')
    attendance = cursor.fetchall()
    data= request.get_json()
    status= data.get('status')
    for data in attendance:
        print(data, date, course_id)
        if(data[0]==student_mail and data[2]==date and data[1]==course_id):
            cursor.execute('''UPDATE dailyattendance
                  SET status = ?
                  WHERE student_mail = ? AND date = ? AND course_id = ?''',
               (status, student_mail, date, course_id))

    cursor.close()
    conn.close()

    return {"message":"modified succesfully"}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # app.run(debug=True)