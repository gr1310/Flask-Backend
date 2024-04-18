from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, jsonify
from sqlalchemy.engine import create_engine
from sqlalchemy import text
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = db.init_app(app)

################################# HOME ########################################
    
@app.route('/', methods=['GET'])
def server_home():
    return "Server home"

################################# REGISTER END POINTS ########################################

@app.route('/student/register', methods=['POST'])
def register_student():
    data = request.get_json()

    student_id = data.get('student_id')
    std_name = data.get('std_name')
    # photo_data = data.get('photo_data')
    department = data.get('department')
    password = data.get('password')
    mobile = data.get('mobile')
    mail = data.get('mail')

    # Check if all required fields are provided
    if not all([student_id, std_name, department, password, mobile, mail]):
        return jsonify({"message": "All fields are required"}), 400

    # Check if student ID or email already exists
    existing_student = Student.query.filter_by(student_id=student_id).first()
    existing_email = Student.query.filter_by(mail=mail).first()
    if existing_student or existing_email:
        return jsonify({"message": "Student ID or email already exists"}), 400

    student = Student(
        student_id=student_id,
        std_name=std_name,
        department=department,
        password=password,
        mobile=mobile,
        mail=mail
    )

    try:
        db.session.add(student)
        db.session.commit()
        return jsonify({"message": "Student registration success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred while registering student"}), 500

@app.route('/teacher/register', methods=['POST'])
def register_instructor():
    data = request.get_json()

    instructor_name = data.get('instructor_name')
    department = data.get('department')
    password = data.get('password')
    mail = data.get('mail')
    mobile = data.get('mobile')

    # Check if all required fields are provided
    if not all([mail, instructor_name, mobile, department, password]):
        return jsonify({"message": "All fields are required"}), 400

    # Check if email already exists
    existing_instructor = Instructor.query.filter_by(mail=mail).first()
    if existing_instructor:
        return jsonify({"message": "Email already exists"}), 400

    # Create and save new instructor
    instructor = Instructor(
        mail=mail,
        instructor_name=instructor_name,
        mobile=mobile,
        department=department,
        password=password
    )

    try:
        db.session.add(instructor)
        db.session.commit()
        return jsonify({"message": "Instructor registration success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred while registering instructor"}), 500

################################# LOGIN END POINTS ########################################
    
@app.route('/student/login', methods=['PUT'])
def student_login():
    data = request.get_json()

    if data == None or 'roll' not in data or 'password' not in data:
        return jsonify({"error": "Invalid request"}), 400

    roll = data['roll']
    password = data['password']

    student = Student.query.filter_by(student_id=roll, password=password).first()
    if student:
        return jsonify({"message": "Login success"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 400

@app.route('/teacher/login', methods=['PUT'])
def teacher_login():
    data = request.get_json()

    if data == None or 'roll' not in data or 'password' not in data:
        return jsonify({"result": False, "error": "Invalid request"}), 400

    roll = data['roll']
    password = data['password']

    instructor = Instructor.query.filter_by(mail=roll, password=password).first()
    if instructor:
        return jsonify({"message": "Login success"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 400

################################# DETAILS ########################################
    
@app.route('/student/details/<roll>', methods=['GET'])
def get_student_details(roll):
    student = Student.query.get(roll)
    if student:
        return jsonify({"username": student.std_name, "dept": student.department}), 200
    else:
        return jsonify({"mssage": "Details Not Found"}), 500

@app.route('/teacher/details/<roll>', methods=['GET'])
def get_teacher_details(roll):
    instructor = Instructor.query.get(roll)
    if instructor:
        return jsonify({"username": instructor.instructor_name, "dept": instructor.department}), 200
    else:
        return jsonify({"message": "Details Not Found"}), 500

################################# GET COURSES ########################################
@app.route('/student/courses', methods=['GET'])
def get_courses():
    try:
        # Query the Takes table for courses taken by the student
        courses_taken = Course.query.all()

        # Extract course IDs from the query result
        course_ids = [course.course_id for course in courses_taken]

        return jsonify(course_ids), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/student/courses/<student_id>')
def get_student_courses(student_id):
    try:
        # Query the Takes table for courses taken by the student
        courses_taken = Takes.query.filter_by(student_id=student_id).all()

        # Extract course IDs from the query result
        course_ids = [course.course_id for course in courses_taken]

        return jsonify(course_ids), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/teacher/courses/<instructor_mail>')
def get_teacher_courses(instructor_mail):
    try:
        # Query the Teaches table for courses taught by the instructor
        taught_courses = Teaches.query.filter_by(instructor_mail=instructor_mail).all()

        # Extract course IDs from the query result
        course_ids = [course.course_id for course in taught_courses]

        return jsonify(course_ids), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
################################# SERVICES ########################################
    
# Create engine
def create_engine_from_flask_config():

    return create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# Define SQLAlchemy session
def get_session():

    engine = create_engine_from_flask_config()
    Session = sessionmaker(bind=engine)
    return Session()

months = {
    1:'Jan',
    2:'Feb',
    3:'Mar',
    4:'Apr',
    5:'May',
    6:'Jun',
    7:'Jul',
    8:'Aug',
    9:'Sep',
    10:'Oct',
    11:'Nov',
    12:'Dec',
}

@app.route('/department_courses/<department_id>')
def get_department_courses(department_id):

    session = get_session()

    try:

        statement = text("SELECT * FROM course WHERE course.dept_id = :dept_id")
        result = session.execute(statement, {'dept_id': department_id}).fetchall()
        courses = {row.course_id: row.course_name for row in result}
        session.close()
        return jsonify(courses)
    
    except Exception as e:

        session.close()
        return jsonify({'error': str(e)}), 500

@app.route('/daily_attendance/<student_id>/<course_id>')
def get_daily_attendance(student_id, course_id):

    session = get_session()

    try:

        statement = text("SELECT * FROM dailyattendance WHERE student_id_id= :std_id AND course_id_id= :course_id;")
        temp = session.get_data_with_values(statement, {'std_id': student_id, 'course_id': course_id})
        
        result = {'dates': [], 'status': []}
        for row in temp:
            result['dates'].append(f"{months.get(row.date.month)}-{row.date.day}")
            result['status'].append(1 if row.status else 0)
        
        session.close()
        return jsonify(result)
    
    except Exception as e:

        session.close()
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)