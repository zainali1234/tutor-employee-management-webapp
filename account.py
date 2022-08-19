# handles all the non-admin / basic user functionalities used by employees of the company
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user
from .models import SessionForm, Employee, Student
from . import db
account = Blueprint('account', __name__)

# automatically renders the homepage when user is logged in
@account.route('/account/home')
@login_required
def home():
    return render_template('home-page.html', user=current_user)

# gives 'logged out' status to the user and redirects to login page when user clicks on 'Log Out' button
@account.route('/account/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# renders the learning session fill out page when user clicks "Fill Out Session"
@account.route('/account/fill-out-session', methods=['GET','POST'])
@login_required
def fill_out_session():
    # if user submits session information, then check conditions to make sure info meets all conditions
    if request.method == 'POST':
        student_name = request.form.get("student-name")
        student_id = "N/A"
        for student in Student.query.all():
            if student.name == student_name:
                student_id = student.id
        subject_name = request.form.get("subject-name")
        time_length = request.form.get("time-length")
        prof_rating = request.form.get("proficiency-level")
        description = request.form.get("description")
        employee_id = current_user.id
        if student_name == "select-name":
            flash('Please select a student name.', category='error')
        elif len(subject_name) < 3:
            flash('Subject name must be more than two characters.', category='error')
        elif len(time_length) < 1:
            flash('Please enter a proficiency rating.', category='error')
        elif int(time_length) < 1:
            flash('Time length must be more than one minutes.', category='error')
        elif len(prof_rating) < 1:
            flash('Please enter a proficiency rating.', category='error')
        elif (int(prof_rating) < 1) or (int(prof_rating) > 5):
            flash('Proficiency rating must be between digits 1-5', category='error')
        elif len(description) < 11:
            flash('Description must be more than 10 characters.', category='error')
        else:
            new_session = SessionForm(student_name=student_name, student_id=student_id, subject_name=subject_name,
                description=description, proficiency_level=int(prof_rating), time_length=int(time_length), employee_id=current_user.id)
            db.session.add(new_session)
            db.session.commit()
            flash('Session successfully submitted!', category='success')
    return render_template('session-fillout-page.html', user=current_user, students=Student.query.all())

# renders the session data page which provides user all sessions that the user has filled out
@account.route('/account/past-session-data')
@login_required
def session_data():
    return render_template('session-data.html', user=current_user)

# allows user to update their account information
@account.route('/account/account-settings', methods=['GET','POST'])
@login_required
def account_settings():
    # if user submits new account information, then check conditions to make sure info meets all conditions
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        if len(username) < 4:
            flash('Username must be greater than 3 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        else:
            # changes the account attributes of the current user within the database 
            current_user.username = username
            current_user.email = email
            current_user.first_name = first_name
            current_user.last_name = last_name
            db.session.commit()
    return render_template('account-settings.html', user=current_user)

