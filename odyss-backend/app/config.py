# config.py
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'FromThe104')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default')
    JWT_HEADER_TYPE = "Bearer"
    JWT_ALGORITHM = "HS256"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/odyss_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 20
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_MAX_OVERFLOW = 20
    PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
    PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    # BREVO_API_KEY = os.getenv("BREVO_API_KEY")
    # BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")


