from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, TextAreaField, SelectField

class AddLog(FlaskForm):
    print('Adding Log')
    date_posted = DateField('Date')
    content = TextAreaField('Log Content')
    remarks = StringField('Remarks')
    submit = SubmitField('Add Log')

class SearchLog(FlaskForm):
    print('Searching Log')
    frequency = SelectField('Frequency', choices=[('frequency', 'Frequency'), ('daily', 'Daily'), ('monthly', 'Monthly'), ('yearly', 'Yearly')])
    date_posted = DateField('Date')
    submit = SubmitField('Search')

class DeleteLog(FlaskForm):
    id = IntegerField('Id No of the Log to be removed')
    submit = SubmitField('Remove Log')
