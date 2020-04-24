from flask import Blueprint, render_template, redirect, url_for, request
from myhome import db
from myhome.models import Logs
from myhome.blogs.forms import AddLog, DeleteLog, SearchLog
from sqlalchemy import extract
import datetime

blogs_blueprints = Blueprint('blogs', __name__, template_folder='templates/blogs')

@blogs_blueprints.route('/add', methods=['GET', 'POST'])
def add():

    form = AddLog()
    if request.method == 'GET':
        print('GET Request to blogs/add')
        logs = Logs.query.filter(db.func.DATE(Logs.date_posted) == datetime.date.today()).all()
    else:
        print('POST Request to blogs/add')
        print(f'Valid form: {form.validate()}')

        if form.validate_on_submit():
            print('Add logs valid')
            date_posted = form.date_posted.data
            content = form.content.data
            remarks = form.remarks.data

            new_log = Logs(date_posted, content, remarks)
            db.session.add(new_log)
            db.session.commit()

            return redirect(url_for('blogs.add'))

    return render_template('addlog.html', logs=logs, form=form)

@blogs_blueprints.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    form = SearchLog()

    if request.method == 'GET':
        print('GET Request to blogs/dashboard')
        logs = Logs.query.all()
        
    else:
        print('POST Request to blogs/dashboard')
        print(f'Valid form: {form.validate()}')

        if form.validate_on_submit():
            frequency = form.frequency.data
            selecteddate = form.date_posted.data
            
            if frequency == 'monthly':
                logs = Logs.query.filter(extract('month', Logs.date_posted) == selecteddate.month).all()
            elif frequency == 'yearly':
                logs = Logs.query.filter(extract('year', Logs.date_posted) == selecteddate.year).all()
            elif frequency == 'daily':
                logs = Logs.query.filter(extract('day', Logs.date_posted) == selecteddate.day).all()
            else:
                logs = Logs.query.filter(db.func.DATE(Logs.date_posted) == datetime.date.today()).all()

    return render_template('logsdashboard.html', logs=logs, form=form)

@blogs_blueprints.route('/delete', methods=['GET', 'POST'])
def delete():

    form = DeleteLog()

    if form.validate_on_submit():
        id = form.id.data
        log = Logs.query.get(id)

        db.session.delete(log)
        db.session.commit()

        return redirect(url_for('blogs.dashboard'))
    return render_template('addlog.html', form=form)
