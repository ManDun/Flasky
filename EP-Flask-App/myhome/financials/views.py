from flask import Blueprint, render_template, redirect, url_for, request, send_file
import datetime
from io import BytesIO
from myhome import db
from myhome.models import Expense, User, Files
from flask_login import current_user,login_required
from myhome.financials.forms import AddExpense, DeleteExpense, SearchExpenses
from sqlalchemy import extract, and_

financials_blueprints = Blueprint('financials', __name__, template_folder='templates/financials')

@financials_blueprints.route('/add', methods=['GET', 'POST'])
def add():

    form = AddExpense()
    user_id = current_user.id
    expenses = []
    if request.method == 'GET':
        print('GET Request to financials/add')
        #expenses = Expense.query.filter(db.func.DATE(Expense.date_of_expense) == datetime.date.today()).filter_by(user_id=user_id).join(Files).filter(Files.expense_id == Expense.id) .all()

        expenses = db.session.query(Expense, Files).outerjoin(Files, Expense.id==Files.expense_id)
        expenses = expenses.filter(and_(db.func.DATE(Expense.date_of_expense) == datetime.date.today(), Expense.user_id == user_id)).all()
        print(f'{len(expenses)} expenses fetched to display')
    else:
        print(f'POST Request to financials/add, form valid: {form.validate()}')
        if form.validate_on_submit():
            name = form.name.data
            type = form.type.data
            amount = form.amount.data
            details = form.details.data
            date_of_expense = form.date_of_expense.data

            new_expense = Expense(name=name, type=type, amount=amount, details=details, date_of_expense=date_of_expense, user_id=user_id)
            db.session.add(new_expense)
            db.session.flush()

            if form.expensefile.data is not None:
                filename = form.expensefile.data.filename
                filetype = form.expensefile.data.mimetype
                filecontents = form.expensefile.data.read()
                filesize = form.expensefile.data.content_length
            
                new_file = Files(name=filename, type=filetype, contents=filecontents, size=filesize, expense_id=new_expense.id)
                db.session.add(new_file)
                db.session.flush()

            print(f'File uploaded for expense id {new_expense.id}')
            db.session.commit()

            return redirect(url_for('financials.add'))

    return render_template('addexpense.html', form=form, expenses=expenses)

@financials_blueprints.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    form = SearchExpenses()
    user_id = current_user.id
    expenses = db.session.query(Expense, Files).outerjoin(Files, Expense.id==Files.expense_id)
    if request.method == 'GET':
        print('GET Request to Financials/dashboard')
        expenses = expenses.filter(and_(db.func.DATE(Expense.date_of_expense) == datetime.date.today()), Expense.user_id==user_id).all()
        
    else:
        print('POST Request to Financials/dashboard')
        print(f'Valid form: {form.validate()}')

        if form.validate_on_submit():
            frequency = form.frequency.data
            selecteddate = form.date_posted.data
            
            if frequency == 'monthly':
                expenses = expenses.filter(and_(extract('month', Expense.date_of_expense) == selecteddate.month), Expense.user_id==user_id).all()
            elif frequency == 'yearly':
                expenses = expenses.filter(and_(extract('year', Expense.date_of_expense) == selecteddate.year), Expense.user_id==user_id).all()
            elif frequency == 'daily':
                expenses = expenses.filter(and_(extract('day', Expense.date_of_expense) == selecteddate.day), Expense.user_id==user_id).all()
            else:
                expenses = expenses.filter(and_(db.func.DATE(Expense.date_of_expense) == datetime.date.today()), Expense.user_id==user_id).all()

            

    return render_template('expensesdashboard.html', expenses=expenses, form=form)

@financials_blueprints.route('/<int:expense_id>/delete', methods=['GET', 'POST'])
def delete(expense_id):

    print(f'Deleting expense id {expense_id}')
    expense = Expense.query.get_or_404(expense_id)
    files = Files.query.filter(expense_id==expense_id).first()
    db.session.delete(expense)
    if files:
        print(f'File {files.name} attached to expense, deleting it')
        db.session.delete(files)
    db.session.commit()

    return redirect(url_for('financials.dashboard'))

@financials_blueprints.route('/<int:file_id>/download', methods=['GET', 'POST'])
def download(file_id):

    print(f'Viewing file id {file_id}')
    files = Files.query.filter_by(id=file_id).first()
    return send_file(BytesIO(files.contents), attachment_filename=files.name, mimetype=files.type, as_attachment=False)
    
