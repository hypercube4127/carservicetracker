import os
import bcrypt
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

def init_default_user():
  try:
    from app.models import User  # Import here to avoid circular import issues
    admin_email = os.getenv('ADMIN_USER_EMAIL')
    if not db.session.query(User).filter_by(email=admin_email).first():
      admin_user = User(
        email=admin_email,
        fullname="Admin",
        password=bcrypt.hashpw(str(os.getenv('ADMIN_USER_DEFAULT_PW')).encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        status=UserStatus.ACTIVE
      )
      db.session.add(admin_user)
      db.session.commit()
  except Exception as e:
    print(f"Could not create default user")

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

# Connected tools
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Importing models and routes (to avoid cross-referencing at the end)

from app.models import *
from app.routes import *

# Initialize the default user
with app.app_context():
    init_default_user()