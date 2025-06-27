# email.py
# notifications/providers/email.py

def send_email(to, subject, message):
    # Dummy logic; in real use, you'd integrate with SendGrid, SMTP, etc.
    print(f"[EMAIL] To: {to} | Subject: {subject} | Message: {message}")
    return {"status": "sent", "method": "email"}
