# utils.py
# app/auth/utils.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return check_password_hash(hashed, password)

def generate_tokens(user):
    identity = user.id  # keep it simple (UUID)
    additional_claims = {
        "email": user.email,
        "name": user.name
    }
    access_token = create_access_token(
        identity=identity,
        additional_claims={},
        expires_delta=timedelta(hours=1)
    )
    refresh_token = create_refresh_token(identity=identity)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

import random
from datetime import datetime, timedelta
from app.extensions import db
from app.models.email_otp import EmailOTP

def generate_otp():
    return f"{random.randint(100000, 999999)}"

def create_and_send_otp(email):
    otp_code = generate_otp()
    expires = datetime.utcnow() + timedelta(minutes=10)

    existing = EmailOTP.query.filter_by(email=email).first()
    if existing:
        existing.otp = otp_code
        existing.expires_at = expires
    else:
        new_otp = EmailOTP(email=email, otp=otp_code, expires_at=expires)
        db.session.add(new_otp)
    db.session.commit()

    # TODO: Send `otp_code` to `email` using your email provider
    print(f"[DEV ONLY] OTP for {email}: {otp_code}")  # Remove in prod
    return otp_code

