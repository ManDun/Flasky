import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from . import consts as const

app = Flask(__name__)
login_manager = LoginManager()

base_dir = os.path.abspath(os.path.dirname(__file__))

dir_path = os.path.dirname(os.path.realpath(__file__))
passfile = os.path.join(dir_path, 'pass')

with open(passfile) as f:
    data = f.read()

password = data.strip()

app.config['SECRET_KEY'] = 'mysecretkey'
db_url = f'postgresql+psycopg2://{const.POSTGRES_USER}:{password}@{const.POSTGRES_URL}/{const.POSTGRES_DB}'
#db_url = 'sqlite:///'+os.path.join(base_dir, 'data.sqllite')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'

from myhome.financials.views import financials_blueprints
from myhome.blogs.views import blogs_blueprints
from myhome.auth.views import auth_blueprints
from myhome.admin.views import admin_blueprints

app.register_blueprint(financials_blueprints, url_prefix='/financials')
app.register_blueprint(blogs_blueprints, url_prefix='/blogs')
app.register_blueprint(auth_blueprints, url_prefix='/auth')
app.register_blueprint(admin_blueprints, url_prefix='/admin')
