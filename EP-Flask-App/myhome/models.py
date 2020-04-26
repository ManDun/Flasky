from myhome import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')
    logs = db.relationship('Logs', backref='author', lazy=True)
    expense = db.relationship('Expense', backref='author', lazy=True)

    def __init__(self, name=None, username=None, email=None, password=None, role=None):
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    content = db.Column(db.Text, nullable=False)
    remarks = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, date_posted=None, content=None, remarks=None, user_id=None):
        self.date_posted = date_posted
        self.content = content
        self.remarks = remarks
        self.user_id = user_id

    def __repr__(self):
        return f"Log('{self.date_posted}', content'{self.content}')"


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    details = db.Column(db.String(260))
    date_of_expense = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    files = db.relationship('Files', backref='source', lazy=True)


    def __init__(self, name=None, type=None, amount=None, details=None, date_of_expense=None, user_id=None):
        self.name = name
        self.type = type
        self.amount = amount
        self.details = details
        self.date_of_expense = date_of_expense
        self.user_id = user_id

    def __repr__(self):
        return f"Expenses('{self.name}', '{self.amount}')"


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    date_of_upload = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    contents = db.Column(db.LargeBinary)
    size = db.Column(db.Float, default=0)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)

    def __init__(self, name=None, type=None, date_of_upload=None, contents=None, size=None, expense_id=None):
        self.name = name
        self.type = type
        self.date_of_upload = date_of_upload
        self.contents = contents
        self.size = size
        self.expense_id = expense_id

    def __repr__(self):
        return f"Files('{self.name}', '{self.id}', '{self.type}')"
