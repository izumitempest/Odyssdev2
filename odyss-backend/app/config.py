# config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change_me')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'change_me_too')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/odyss_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 20
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_MAX_OVERFLOW = 20
