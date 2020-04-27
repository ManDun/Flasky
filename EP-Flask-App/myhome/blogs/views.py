from flask import Blueprint, render_template, redirect, url_for, request
from myhome import db
from myhome.models import Logs, User
from myhome.blogs.forms import AddLog, DeleteLog, SearchLog
from flask_login import current_user,login_required
from sqlalchemy import extract
import datetime

blogs_blueprints = Blueprint('blogs', __name__, template_folder='templates/blogs')


@blogs_blueprints.route('/add', methods=['GET', 'POST'])
def add():

    if current_user.is_authenticated:
        print('User authenticated')
        form = AddLog()
        user_id = current_user.id
        if request.method == 'GET':
            print('GET Request to blogs/add')
            logs = Logs.query.filter(db.func.DATE(Logs.date_posted) == datetime.date.today()).filter_by(user_id=user_id).all()
        else:
            print('POST Request to blogs/add')
            print(f'Valid form: {form.validate()}')

            if form.validate_on_submit():
                print('Add logs valid')
                date_posted = form.date_posted.data
                content = form.content.data
                remarks = form.remarks.data

                new_log = Logs(date_posted, content, remarks, user_id=user_id)
                db.session.add(new_log)
                db.session.commit()

                return redirect(url_for('blogs.add'))

        return render_template('addlog.html', logs=logs, form=form)
    else:
        print('User tried accessing blogs.add and not authenticated')
        return redirect(url_for('auth.login'))

@blogs_blueprints.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if current_user.is_authenticated:
        print('User authenticated')
        form = SearchLog()
        user_id = current_user.id
        if request.method == 'GET':
            print('GET Request to blogs/dashboard')
            logs = Logs.query.filter(db.func.DATE(Logs.date_posted) == datetime.date.today()).filter_by(user_id=user_id).all()
            
        else:
            print('POST Request to blogs/dashboard')
            print(f'Valid form: {form.validate()}')

            if form.validate_on_submit():
                frequency = form.frequency.data
                selecteddate = form.date_posted.data
                
                if frequency == 'monthly':
                    logs = Logs.query.filter(extract('month', Logs.date_posted) == selecteddate.month).filter_by(user_id=user_id).all()
                elif frequency == 'yearly':
                    logs = Logs.query.filter(extract('year', Logs.date_posted) == selecteddate.year).filter_by(user_id=user_id).all()
                elif frequency == 'daily':
                    logs = Logs.query.filter(extract('day', Logs.date_posted) == selecteddate.day).filter_by(user_id=user_id).all()
                else:
                    logs = Logs.query.filter(db.func.DATE(Logs.date_posted) == datetime.date.today()).filter_by(user_id=user_id).all()

            else:
                logs = Logs.query.filter(db.func.DATE(Logs.date_posted) == datetime.date.today()).filter_by(user_id=user_id).all()
                error = 'Please enter required details and then submit!'

        return render_template('logsdashboard.html', logs=logs, form=form, error=error)
    else:
        print('User tried accessing blogs.dashboard and not authenticated')
        return redirect(url_for('auth.login'))
    
@blogs_blueprints.route('/<int:log_id>/delete', methods=['GET', 'POST'])
def delete(log_id):

    if current_user.is_authenticated:
        print('User authenticated')
        print(f'Deleting log id {log_id}')
        log = Logs.query.get_or_404(log_id)
        db.session.delete(log)
        db.session.commit()

        return redirect(request.referrer)
    else:
        print('User tried accessing blogs.dashboard and not authenticated')
        return redirect(url_for('auth.login'))
