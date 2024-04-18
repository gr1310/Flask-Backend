from flask_sqlalchemy import SQLAlchemy
import base64

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.String(50), primary_key=True)
    std_name = db.Column(db.String(50))
    photo = db.Column(db.Text, default='', nullable=True)
    department = db.Column(db.String(50))
    password = db.Column(db.String(50))
    mobile = db.Column(db.String(15))
    mail = db.Column(db.String(50))
    takes = db.relationship('Takes', backref='student', cascade='all, delete-orphan')
    daily_attendance = db.relationship('DailyAttendance', backref='student', cascade='all, delete-orphan')

    def save_photo(self, photo_data):
        img_data = base64.b64decode(photo_data)
        with open(f'images/{self.student_id}.png', 'wb') as f:
            f.write(img_data)
        self.photo = f'images/{self.student_id}.png'

class Instructor(db.Model):
    __tablename__ = 'instructor'
    mail = db.Column(db.String(50), primary_key=True)
    instructor_name = db.Column(db.String(50))
    mobile = db.Column(db.String(15))
    department = db.Column(db.String(50))
    password = db.Column(db.String(50))

class Department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.String(5), primary_key=True)
    dept_name = db.Column(db.String(50))
    courses = db.relationship('Course', backref='department', cascade='all, delete-orphan')

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.String(50), primary_key=True)
    course_name = db.Column(db.String(50))
    dept_id = db.Column(db.String(5), db.ForeignKey('department.dept_id', ondelete='CASCADE'))
    takes = db.relationship('Takes', backref='course', cascade='all, delete-orphan')
    daily_attendance = db.relationship('DailyAttendance', backref='course', cascade='all, delete-orphan')

class Takes(db.Model):
    __tablename__ = 'takes'
    student_id = db.Column(db.String(50), db.ForeignKey('student.student_id', ondelete='CASCADE'), primary_key=True)
    course_id = db.Column(db.String(50), db.ForeignKey('course.course_id', ondelete='CASCADE'), primary_key=True)
    grade = db.Column(db.String(5), nullable=True)
    attendance_percentage = db.Column(db.Integer, default=100)

class Teaches(db.Model):
    __tablename__ = 'teaches'
    id = db.Column(db.Integer, primary_key=True)
    instructor_mail = db.Column(db.String(50), db.ForeignKey('instructor.mail', ondelete='CASCADE'))
    course_id = db.Column(db.String(50), db.ForeignKey('course.course_id', ondelete='CASCADE'))
    num_students = db.Column(db.Integer, nullable=True)

class DailyAttendance(db.Model):
    __tablename__ = 'dailyattendance'
    student_id = db.Column(db.String(50), db.ForeignKey('student.student_id', ondelete='CASCADE'), primary_key=True)
    course_id = db.Column(db.String(50), db.ForeignKey('course.course_id', ondelete='CASCADE'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    status = db.Column(db.Boolean)