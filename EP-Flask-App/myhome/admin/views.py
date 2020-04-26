from flask import Blueprint, render_template, redirect, url_for, request, send_file
import datetime
from myhome import db
from myhome.models import User
from flask_login import current_user,login_required
from sqlalchemy import extract, and_

admin_blueprints = Blueprint('admin', __name__, template_folder='templates/admin')

@admin_blueprints.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    user_id = current_user.id
    if request.method == 'GET':
        print('GET Request to admin/dashboard')
        users = User.query.all()    

    return render_template('usersdashboard.html', users=users)

@admin_blueprints.route('/<int:user_id>/delete', methods=['GET', 'POST'])
def delete(user_id):

    cur_user_id = current_user.id
    if cur_user_id == user_id:
        users = User.query.all()  
        return render_template('usersdashboard.html', users=users)
    else:
        print(f'Deleting user id {user_id}')
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('admin.dashboard'))