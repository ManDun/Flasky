from myhome import db
from flask import render_template,redirect,request,url_for,flash,abort,Blueprint
from flask_login import login_user,login_required, logout_user, current_user
from myhome.models import User
from myhome.auth.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import extract
import datetime

auth_blueprints = Blueprint('auth', __name__, template_folder='templates/auth')

@auth_blueprints.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@auth_blueprints.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You Logged Out!')
    return redirect(url_for('home'))

@auth_blueprints.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    error = None

    if request.method == 'GET':
        print('GET Request to auth/login')
    else:
        print('POST Request to auth/login')
        print(f'Valid form: {form.validate()}')

        if form.validate_on_submit():
            print('Login User')
            user = User.query.filter_by(email=form.email.data).first()

            if user is not None and user.check_password(form.password.data) :
                login_user(user)
                flash('Login Succesful!')

                next = request.args.get('next')

                if next is None or not next[0] == '/':
                    next = url_for('auth.welcome_user')

                return redirect(next)
            else:
                error = 'Invalid Username or Password'

    return render_template('login.html', form=form, error=error)

@auth_blueprints.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if request.method == 'GET':
        print('GET Request to auth/register')
    else:
        print('POST Request to auth/register')
        print(f'Valid form: {form.validate()}')

        if form.validate_on_submit():
            print('Login User')
            user = User(name=form.name.data,
                            email=form.email.data,
                            username=form.username.data,
                            password=form.password.data
                            )

            db.session.add(user)
            db.session.commit()
            print(f'User {user.email} registered succesfully')
            flash('Succesfully registered!')

            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_blueprints.route('/profile', methods=['GET', 'POST'])
def profile():

    user_id = current_user.id
    if request.method == 'GET':
        print('GET Request to auth/profile')
    else:
        print('POST Request to auth/profile')

    return render_template('userprofile.html', user=current_user)

@auth_blueprints.route('/settings', methods=['GET', 'POST'])
def settings():

    user_id = current_user.id
    if request.method == 'GET':
        print('GET Request to auth/settings')
    else:
        print('POST Request to auth/settings')

    return render_template('usersettings.html', user=current_user)
