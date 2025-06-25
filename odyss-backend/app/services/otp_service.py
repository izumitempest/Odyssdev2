import random
from datetime import datetime, timedelta
from app.extensions import db
from app.models.email_otp import EmailOTP  # adjust import if needed

def generate_otp(length: int = 6) -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def generate_and_store_otp(email: str, otp: str = None) -> str:
    otp = otp or generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=10)

    # Delete old OTPs for that email (1 OTP/email rule)
    existing = EmailOTP.query.filter_by(email=email).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()

    new_otp = EmailOTP(email=email, otp=otp, expires_at=expiry)
    db.session.add(new_otp)
    db.session.commit()

    return otp

def verify_otp(email: str, input_otp: str) -> bool:
    record = EmailOTP.query.filter_by(email=email).first()
    if not record:
        return False
    if record.is_expired():
        db.session.delete(record)
        db.session.commit()
        return False
    if record.otp != input_otp:
        return False

    # OTP is valid — consume it
    db.session.delete(record)
    db.session.commit()
    return True
