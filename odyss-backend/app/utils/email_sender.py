# import resend
# from flask import current_app

# resend.api_key = current_app.config["RESEND_API_KEY"]

# def send_otp_email(to_email: str, otp: str) -> bool:
#     try:
#         resend.Emails.send({
#             "from": "Odyss <no-reply@odyss.ng>",  # use a verified domain or Resend default
#             "to": [to_email],
#             "subject": "Your Odyss Verification OTP",
#             "html": f"<p>Your OTP is: <strong>{otp}</strong></p><p>This code will expire in 10 minutes.</p>",
#         })
#         return True
#     except Exception as e:
#         print("❌ Failed to send OTP email:", e)
#         return False

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv

load_dotenv()  # Load SENDGRID_API_KEY from .env

FROM_EMAIL = "no-reply@odyss.ng"

def send_otp_email(recipient_email: str, otp: str) -> bool:
    subject = "Your Odyss Verification Code 🚀"
    html_content = f"""
        <html>
            <body style="font-family:sans-serif;">
                <h2>Hello from Odyss 👋</h2>
                <p>Your OTP code is:</p>
                <h1 style="letter-spacing:4px; color:#4CAF50;">{otp}</h1>
                <p>This code is valid for 10 minutes. If you didn’t request this, ignore it.</p>
                <br/>
                <small>— Team Odyss 💼</small>
            </body>
        </html>
    """
    plain_text = f"Your Odyss OTP is: {otp}. Valid for 10 minutes."

    message = Mail(
        from_email=Email(FROM_EMAIL, "Odyss Verification"),
        to_emails=To(recipient_email),
        subject=subject,
        plain_text_content=Content("text/plain", plain_text),
        html_content=Content("text/html", html_content)
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"[SENDGRID] OTP email sent to {recipient_email} (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"[SENDGRID ERROR] Failed to send email: {e}")
        return False
