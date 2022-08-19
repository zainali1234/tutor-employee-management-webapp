from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Employee
from . import db
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/')
def redirect_login():
    if current_user.is_authenticated:
        return redirect('/account/home')
    else:
        return redirect('/login')

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        employee = Employee.query.filter_by(username=username).first() #gets account associated with username
        if employee:
            if check_password_hash(employee.password, password):
                # remembers that employee is logged in
                login_user(employee, remember=True)
                return redirect(url_for('account.home'))
            else:
                flash('Incorrect password, please try again', category='error')
        else:
            flash('Account does not exist.', category='error')
    return render_template('login-portal.html', user=current_user)

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        username = request.form.get('username')
        password_1 = request.form.get('password1')
        password_2 = request.form.get('password2')
        admin_status = eval(request.form.get('admin_status_select'))
        employee_username = Employee.query.filter_by(username=username).first()
        employee_email = Employee.query.filter_by(email=email).first()

        if len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif employee_email and not employee_username:
            flash('Account with this email already exists.', category='error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters.', category='error')
        elif employee_username and not employee_email:
            flash('Account with this username already exists.', category='error')
        elif password_1 != password_2:
            flash('Passwords don\'t match.', category='error')
        elif len(password_1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_employee = Employee(first_name=first_name, last_name=last_name, email=email, username=username, password=generate_password_hash(password_1, method='sha256'), admin_status=admin_status)
            db.session.add(new_employee)
            db.session.commit()
            login_user(new_employee, remember=True)
            return redirect(url_for('account.home'))
    return render_template('sign-up-portal.html')
