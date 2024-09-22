import os
import toml
from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta

# load environment variables from environment and .env file
load_dotenv()

def load_pyproject_toml():
    with open('./pyproject.toml', 'r') as f:
        return toml.load(f)

project_config = load_pyproject_toml()

# Flask Initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_HTTPONLY'] = True
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=int(os.getenv('JWT_EXPIRE_IN_MINUTES', 60)))
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'materia'

# Connected tools
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Importing models and routes (to avoid cross-referencing at the end)
from app import routes
from app.auth import routes
from app.users import models, routes