from flask import Blueprint, render_template, redirect, url_for, request, send_file
import datetime
from myhome import db
from myhome.models import User
from flask_login import current_user,login_required
from sqlalchemy import extract, and_

admin_blueprints = Blueprint('admin', __name__, template_folder='templates/admin')

@admin_blueprints.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated and current_user.role == 'admin':
        user_id = current_user.id
        print(f'User authenticated {current_user.username} and accessed dashboard in admin')
        if request.method == 'GET':
            print('GET Request to admin/dashboard')
            users = User.query.all()    

        return render_template('usersdashboard.html', users=users)
    else:
        print('User tried accessing admin.dashboard and not authorized')
        return redirect(url_for('auth.login'))

@admin_blueprints.route('/<int:user_id>/delete', methods=['GET', 'POST'])
def delete(user_id):

    if current_user.is_authenticated and current_user.role == 'admin':
        cur_user_id = current_user.id
        print(f'User authenticated {current_user.username} and deleting {user_id} in admin')
        if cur_user_id == user_id:
            print(f'User {current_user.username} cant delete itself')
            users = User.query.all()  
            return render_template('usersdashboard.html', users=users)
        else:
            print(f'Deleting user id {user_id}')
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()

        return redirect(request.referrer)
    else:
        print('User tried accessing admin.delete and not authorized')
        return redirect(url_for('auth.login'))
