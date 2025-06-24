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


import resend
from flask import current_app, request
import requests
import os
from dotenv import load_dotenv
load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
print("🔐 Resend API Key Loaded:", bool(RESEND_API_KEY))

def send_otp_email(email, otp):
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "lilice308@gmail.com",  # Use this unless you're verified
                "to": [email],
                "subject": "Your Odyss OTP Code",
                "html": f"<p>Your OTP is: <strong>{otp}</strong></p>",
            }
        )

        print("📨 Resend response:", response.status_code, response.text)

        return response.status_code == 200

    except Exception as e:
        print("❌ Exception caught while sending email:", e)
        return False
