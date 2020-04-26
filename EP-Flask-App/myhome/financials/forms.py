from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, IntegerField, SubmitField, DateField, DecimalField,TextAreaField, SelectField

class AddExpense(FlaskForm):
    date_of_expense = DateField('Date Of Expense')
    name = StringField('Name of Expense')
    type = StringField('Type of Expense')
    amount = DecimalField('Expense Amount')
    details = TextAreaField('Details')
    expensefile = FileField('Expense File')
    submit = SubmitField('Add Expense')

class SearchExpenses(FlaskForm):
    print('Searching Expenses')
    frequency = SelectField('Frequency', choices=[('frequency', 'Frequency'), ('daily', 'Daily'), ('monthly', 'Monthly'), ('yearly', 'Yearly')])
    date_posted = DateField('Date')
    submit = SubmitField('Search')

class DeleteExpense(FlaskForm):
    id = IntegerField('Id No of the expense to be removed')
    submit = SubmitField('Delete Expense')
