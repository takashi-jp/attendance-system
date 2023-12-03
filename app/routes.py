from flask import render_template, redirect, url_for, abort
from app import app, db
from app.models import Employee, AttendanceRecord
from app.forms import LoginForm, RegisterForm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user


@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.is_admin:
        return redirect(url_for('admin'))
    if not current_user.is_admin:
        return redirect(url_for('employee'))
    else:
        abort(403)

@app.route('/admin')
def admin():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if not current_user.is_admin:
        abort(403)
    employees = Employee.query.all()
    records = AttendanceRecord.query.all() 
    return render_template('admin_dashboard.html', employees=employees, records=records)

@app.route('/employee')
def employee():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # Check if employee has checked in
    latest_record = AttendanceRecord.query.filter_by(employee_id=current_user.id).order_by(AttendanceRecord.check_in_time.desc()).first()
    checked_in = False
    checked_in_time = None
    if latest_record and not latest_record.check_out_time:
        checked_in = True
        checked_in_time = latest_record.check_in_time
    employee = current_user
    return render_template('home.html', employee=employee, checked_in=checked_in, checked_in_time=checked_in_time)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_admin:
        abort(403)
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = Employee(name=form.username.data, email=form.email.data, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/check_in/<int:employee_id>')
def check_in(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    record = AttendanceRecord(employee_id=employee.id, check_in_time=datetime.now())
    db.session.add(record)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/check_out/<int:employee_id>')
def check_out(employee_id):
    record = AttendanceRecord.query.filter_by(employee_id=employee_id).order_by(AttendanceRecord.check_in_time.desc()).first()
    if record and not record.check_out_time:
        record.check_out_time = datetime.now()
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))