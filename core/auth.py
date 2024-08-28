from flask import Flask, jsonify, request, render_template, send_file, redirect, url_for, Blueprint, flash
from flask_login import login_user, logout_user, current_user, login_required
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User

auth = Blueprint('auth', __name__)



@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('username')
        password = request.form.get('password')
        

        # Validation
        if len(email) < 3 or '@' not in email:
            flash('Enter a valid email address', category='error')
        elif len(user_name) < 5:
            flash('user name must be greater than 4 characters', category='error')
        elif len(password) < 5:
            flash('Password must be at least 5 characters', category='error')
        else:
            try:
                user = User.query.filter_by(email=email).first()
                if user:
                    flash('User with this email already exists', category='error')
                else:
                    new_user = User(user_name=user_name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Sign up successful', category='success')
                    return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Database error: {str(e)}', category='error')

    return render_template('signup.html')

@auth.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Succesfully logged in', category='success')
                return redirect(url_for('main.convert'))
            else:
                flash('passwords incorrect', category='error')
        flash('user with email not found', category='error')
    return render_template('login.html')
@auth.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')


@auth.route('/all-users')
def users():
    users = User.query.all()
    return render_template('user.html', users = users)


    

