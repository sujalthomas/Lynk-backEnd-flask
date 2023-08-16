import os
import secrets

import redis

class DefaultConfig:
    # Secret Key
    SECRET_KEY = os.getenv("SECRET_KEY", default=secrets.token_urlsafe(16))
    
    # Database
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Mail
    MAIL_SERVER = "smtp.sendgrid.net"
    MAIL_PORT = 587  # 465 for TLS
    MAIL_USERNAME = "apikey"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # Session
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = "your_app:"
    SESSION_REDIS = redis.StrictRedis(
        host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379), db=0
    )
    
    # Add other configurations as needed
