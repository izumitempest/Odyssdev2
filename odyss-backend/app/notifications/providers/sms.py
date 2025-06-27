# sms.py
# notifications/providers/sms.py

def send_sms(to, message):
    # Integrate Twilio or whatever you like
    print(f"[SMS] To: {to} | Message: {message}")
    return {"status": "sent", "method": "sms"}
