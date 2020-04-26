from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, IntegerField, SubmitField, DateField, DecimalField,TextAreaField, SelectField

class DeleteUser(FlaskForm):
    id = IntegerField('Id No of the expense to be removed')
    submit = SubmitField('Delete Expense')
