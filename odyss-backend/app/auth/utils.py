# utils.py
# app/auth/utils.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
import jwt
from datetime import datetime, timedelta
import os
import dotenv


dotenv.load_dotenv()

def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(input_password, stored_hash):
    return check_password_hash(stored_hash, input_password)
  # move this to config/env

def generate_tokens(user):
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "email": user.email,
            "role": user.role.name if user.role else "user"
        },
        expires_delta=timedelta(hours=1)
    )

    refresh_token = create_refresh_token(
        identity=str(user.id),
        expires_delta=timedelta(days=7)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
# import random
# from datetime import datetime, timedelta
# from app.extensions import db
# from app.models.email_otp import EmailOTP

# def generate_otp():
#     return f"{random.randint(100000, 999999)}"

# def create_and_send_otp(email):
#     otp_code = generate_otp()
#     expires = datetime.utcnow() + timedelta(minutes=10)

#     existing = EmailOTP.query.filter_by(email=email).first()
#     if existing:
#         existing.otp = otp_code
#         existing.expires_at = expires
#     else:
#         new_otp = EmailOTP(email=email, otp=otp_code, expires_at=expires)
#         db.session.add(new_otp)
#     db.session.commit()

#     # TODO: Send `otp_code` to `email` using your email provider
#     print(f"[DEV ONLY] OTP for {email}: {otp_code}")  # Remove in prod
#     return otp_code

# app/auth/utils.py
# app/utils/email_utils.py
# import sib_api_v3_sdk
# from sib_api_v3_sdk.rest import ApiException
# import os
# from flask import current_app

# def send_otp_email(to_email: str, otp: str):
#     configuration = sib_api_v3_sdk.Configuration()
#     configuration.api_key['api-key'] = current_app.config["BREVO_API_KEY"]

#     api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
#     subject = "Your Odyss OTP Code 🚀"
#     sender = {"name": "Odyss", "email": current_app.config["BREVO_SENDER_EMAIL"]}
#     to = [{"email": to_email}]
#     html_content = f"<h2>🔐 Your OTP is: <code>{otp}</code></h2><p>Valid for 10 minutes.</p>"

#     send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#         to=to,
#         html_content=html_content,
#         sender=sender,
#         subject=subject
#     )

#     try:
#         api_response = api_instance.send_transac_email(send_smtp_email)
#         return True
#     except ApiException as e:
#         print(f"❌ Failed to send email: {e}")
#         return False


# 

# app/auth/utils.py
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.models.email_otp import EmailOTP
from app.extensions import db
from app.config import Config
from datetime import datetime, timedelta, timezone
from app.utils.otp import generate_otp

def send_otp_email(email, otp):
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=10)

    # Replace or create OTP record

    record = EmailOTP.query.filter_by(email=email).first()
    if record:
        record.otp = otp
        record.expires_at = expires
        record.created_at = now
    else:
        record = EmailOTP(email=email, otp=otp, expires_at=expires, created_at=now)
        db.session.add(record)

    db.session.commit()

    # Send the OTP email
    message = Mail(
        from_email=Config.EMAIL_FROM,
        to_emails=email,
        subject="Your Odyss Verification Code",
        html_content=f"<h2>🔐 Your OTP is: <strong>{otp}</strong></h2><p>This code expires in 10 minutes.</p>"
    )
    try:
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print("❌ Failed to send email:", str(e))
        return False
