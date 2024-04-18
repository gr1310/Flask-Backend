from flask_sqlalchemy import SQLAlchemy
import base64

db = SQLAlchemy()

class ImageRotator(db.Model):
    __tablename__ = 'image_rotator'
    course_id= db.Column(db.String(50), primary_key=True)
    course_name = db.Column(db.String(50))
    image_data = db.Column(db.String(30000))
    date = db.Column(db.Date)
