from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail as FlaskMail
from flask_security import Security
from flask_session import Session
import os
import secrets
from dotenv import load_dotenv, find_dotenv
import redis
from flask_cors import CORS
import logging 
from itsdangerous import URLSafeTimedSerializer

#initializations

app = Flask(__name__) #
load_dotenv() 

sess = Session()
sess.init_app(app)
mail = FlaskMail(app)

# Database configurations
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Session configurations 
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "your_app:"
app.config["SESSION_REDIS"] = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379), db=0
)

CORS(
    app,
    resources={r"/*": {"origins": ["https://www.linkedin.com"]}},
    supports_credentials=True,
)

# Database configuration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Secuirty configurations
SECRET_KEY = os.getenv("SECRET_KEY", default=secrets.token_urlsafe(16))
app.config["SECRET_KEY"] = SECRET_KEY
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

app.config["SECURITY_PASSWORD_SALT"] = os.getenv(
    "SECURITY_PASSWORD_SALT", default="your_random_salt"
)
app.config["SECURITY_REGISTERABLE"] = True
app.config["SECURITY_RECOVERABLE"] = True
app.config["SECURITY_PASSWORD_SALT"] = os.getenv(
    "SECURITY_PASSWORD_SALT", default="your_random_salt"
)

# Mail Configurations
app.config["YOUR_SENDGRID_API_KEY"] = os.getenv("SENDGRID_API_KEY")
app.config["MAIL_SERVER"] = "smtp.sendgrid.net"
app.config["MAIL_PORT"] = 587  # 465 for TLS
app.config["MAIL_USERNAME"] = "apikey"
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

# Current folder path
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Configuration options
app.config["SECURITY_REGISTERABLE"] = True
app.config["SECURITY_RECOVERABLE"] = True
app.config["SECURITY_TRACKABLE"] = True
logging.basicConfig(level=logging.INFO)

# Configuring Flask-Security with the custom registration form
app.config["SECURITY_REGISTER_USER_TEMPLATE"] = "security/register_user.html"
app.config["SECURITY_REGISTERABLE"] = True
app.config["SECURITY_CONFIRMABLE"] = True
app.config["SECURITY_RECOVERABLE"] = True
app.config["SECURITY_REGISTER_USER_TEMPLATE"] = "security/register_user.html"
app.config["SECURITY_LOGIN_USER_TEMPLATE"] = "security/login_user.html"

# Generate DB tables
with app.app_context():
    db.create_all()

# Import routes after initializing extensions to avoid circular imports
from . import routes