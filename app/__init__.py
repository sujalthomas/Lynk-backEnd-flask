from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail as FlaskMail
from flask_security import Security
from flask_session import Session
import os
import secrets
from dotenv import load_dotenv, find_dotenv
import redis

# Initialize Flask App
app = Flask(__name__)
load_dotenv(find_dotenv())

# Database configuration
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Session configurations
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "your_app:"
app.config["SESSION_REDIS"] = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379), db=0
)
sess = Session()
sess.init_app(app)

# Mail Configurations
app.config["MAIL_SERVER"] = "smtp.sendgrid.net"
app.config["MAIL_PORT"] = 587  # 465 for TLS
app.config["MAIL_USERNAME"] = "apikey"
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

# Initialize extensions
db = SQLAlchemy(app)
mail = FlaskMail(app)


# Import routes after initializing extensions to avoid circular imports
from . import routes