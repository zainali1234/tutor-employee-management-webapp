from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user
from .models import SessionForm, Employee, Student
from . import db
admin = Blueprint('admin', __name__)

@admin.route('/account/employee-database')
@login_required
def employee_database():
    return render_template('admin-employee-database.html', user=current_user, employees=Employee.query.all(), sessions=SessionForm.query.all())

@admin.route('/account/session-database')
@login_required
def session_database():
    return render_template('admin-session-database.html', user=current_user, employees=Employee.query.all(), sessions=SessionForm.query.all())

@admin.route('/account/manage-student-database')
@login_required
def manage_student_database():
    return render_template('admin-manage-student-database.html', user=current_user, employees=Employee.query.all(), sessions=SessionForm.query.all(),
                           students=Student.query.all())

@admin.route('/account/manage-employee-database')
@login_required
def manage_employee_database():
    return render_template('admin-manage-employee-database.html', user=current_user, employees=Employee.query.all(), sessions=SessionForm.query.all(),
                           students=Student.query.all())

@admin.route('/account/delete-employee', methods=['GET','POST'])
@login_required
def delete_employee_database():
    if request.method == 'POST':
        employee_id = request.form.get("delete-employee-id")
        Employee.query.filter(Employee.id == employee_id).delete()
        db.session.commit()
    return render_template('admin-delete-employee.html', user=current_user, employees=Employee.query.all(), sessions=SessionForm.query.all(),
                           students=Student.query.all())

@admin.route('/account/manage-session-database')
@login_required
def manage_session_database():
    return render_template('admin-manage-session-database.html', user=current_user, employees=Employee.query.all(), sessions=SessionForm.query.all(),
                           students=Student.query.all())

@admin.route('/account/delete-session', methods=['GET','POST'])
@login_required
def delete_session_database():
    if request.method == 'POST':
        session_id = request.form.get("delete-session-id")
        SessionForm.query.filter(SessionForm.id == session_id).delete()
        db.session.commit()
    return render_template('admin-delete-session.html', user=current_user, employees=Employee.query.all(), sessions=SessionForm.query.all(),
                           students=Student.query.all())

@admin.route('/account/student-database', methods=['GET','POST'])
@login_required
def student_database():
    return render_template('admin-student-database.html', user=current_user, employees=Employee.query.all(),
                           sessions=SessionForm.query.all(), students=Student.query.all())

@admin.route('/account/register-student', methods=['GET','POST'])
@login_required
def register_student():
    if request.method == 'POST':
        student_name = request.form.get("student-name")
        grade_level = request.form.get("grade-level")
        student_age = request.form.get("student-age")
        parent_name = request.form.get("parent-name")
        parent_email = request.form.get("parent-email")
        other_info = request.form.get("other-info")
        print(other_info)
        if other_info == "":
            other_info = "N/A"
        if len(student_name) < 3:
            flash('Student name must be greater than 2 characters.', category='error')
        elif len(grade_level) < 1:
            flash('Grade level must be greater than 2 characters.', category='error')
        elif int(student_age) < 5:
            flash('Student must be older than 4 to register.', category='error')
        elif len(parent_name) < 2:
            flash('Parent name must be greater than 2 characters.', category='error')
        elif len(parent_email) < 2:
            flash('Email must be greater than 2 characters.', category='error')
        else:
            new_student = Student(name=student_name, grade_level=grade_level,
                                  age=student_age, parent_name=parent_name, parent_email=parent_email,
                                  active_status=True, other_information=other_info)
            db.session.add(new_student)
            db.session.commit()
            flash('Student successfully registered!', category='success')
    return render_template('admin-register-student.html', user=current_user, employees=Employee.query.all(),
                           sessions=SessionForm.query.all(), students=Student.query.all())

@admin.route('/account/delete-student', methods=['GET','POST'])
@login_required
def delete_student_database():
    if request.method == 'POST':
        student_id = request.form.get("delete-student-id")
        Student.query.filter(Student.id == student_id).delete()
        db.session.commit()
    return render_template('admin-delete-student.html', user=current_user, employees=Employee.query.all(), sessions=SessionForm.query.all(),
                           students=Student.query.all())


