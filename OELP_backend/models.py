from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import base64


db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student'
    mail = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    photo = db.Column(db.Text, default='', nullable=True)

    @staticmethod
    def save_image(mail, base64_data):
        try:
            image_data = base64.b64decode(base64_data)
            with open(f'students/{mail}.jpeg', 'wb') as f:
                f.write(image_data)
            return True
        except Exception as e:
            print(f'Error saving image: {str(e)}')
            return False

class Instructor(db.Model):
    __tablename__ = 'instructor'
    mail = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))

class Takes(db.Model):
    __tablename__ = 'takes'
    student_mail = db.Column(db.String(50), db.ForeignKey('student.mail'), primary_key=True)
    course_id = db.Column(db.String(50), db.ForeignKey('course.id'), primary_key=True)
    attendance_percentage = db.Column(db.Integer, default=100)

class Teaches(db.Model):
    __tablename__ = 'teaches'
    instructor_mail = db.Column(db.String(50), db.ForeignKey('instructor.mail'), primary_key=True)
    course_id = db.Column(db.String(50), db.ForeignKey('course.id'), primary_key=True)

class DailyAttendance(db.Model):
    __tablename__ = 'dailyattendance'
    student_mail = db.Column(db.String(50), db.ForeignKey('student.mail'), primary_key=True)
    course_id = db.Column(db.String(50), db.ForeignKey('course.id'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    status = db.Column(db.Boolean)