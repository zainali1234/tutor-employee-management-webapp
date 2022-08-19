from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    grade_level = db.Column(db.String(10))
    age = db.Column(db.Integer)
    parent_name = db.Column(db.String(50))
    parent_email = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    active_status = db.Column(db.Boolean)
    other_information = db.Column(db.String(200))

class SessionForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student_name = db.Column(db.String(50))
    subject_name = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String(500))
    proficiency_level = db.Column(db.Integer)
    time_length = db.Column(db.Integer)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    admin_status = db.Column(db.Boolean)
    session_forms = db.relationship('SessionForm')
