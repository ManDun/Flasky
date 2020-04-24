from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, DecimalField, FileField

class addExpense(FlaskForm):
    date_of_expense = DateField('Date Of Expense')
    name = StringField('Name of Expense')
    type = StringField('Type of Expense')
    amount = DecimalField('Expense Amount')
    details = StringField('Details')
    expensefile = FileField('Expense File')
    submit = SubmitField('Add Expense')

class deleteExpense(FlaskForm):
    id = IntegerField('Id No of the expense to be removed')
    submit = SubmitField('Delete Expense')
