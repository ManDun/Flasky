from flask import Blueprint, render_template, redirect, url_for
from myhome import db
from myhome.models import Expense
from myhome.financials.forms import addExpense, deleteExpense

financials_blueprints = Blueprint('financials', __name__, template_folder='templates/financials')

@financials_blueprints.route('/add', methods=['GET', 'POST'])
def add():

    form = addExpense()

    if form.validate_on_submit():
        name = form.name.data
        type = form.name.data
        amount = form.name.data
        details = form.name.data
        date_of_expense = form.name.data
        expensefile = form.name.data

        new_expense = Expense(name, type, amount, details, date_of_expense, expensefile)
        db.session.add(new_expense)
        db.session.commit()

        return redirect(url_for('financials.list'))
    return render_template('addexpense.html', form=form)

@financials_blueprints.route('/list')
def list():
    expenses = Expense.query.all()
    return render_template('listexpense.html', expenses=expenses)

@financials_blueprints.route('/delete', methods=['GET', 'POST'])
def delete():

    form = deleteExpense()

    if form.validate_on_submit():
        id = form.id.data
        expense = Expense.query.get(id)

        db.session.delete(expense)
        db.session.commit()

        return redirect(url_for('financials.list'))
    return render_template('addexpense.html', form=form)
