import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

base_dir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base_dir, 'data.sqllite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'

from myhome.financials.views import financials_blueprints
from myhome.blogs.views import blogs_blueprints
from myhome.auth.views import auth_blueprints

app.register_blueprint(financials_blueprints, url_prefix='/financials')
app.register_blueprint(blogs_blueprints, url_prefix='/blogs')
app.register_blueprint(auth_blueprints, url_prefix='/auth')
