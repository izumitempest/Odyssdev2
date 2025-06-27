# push.py
# notifications/providers/push.py

def send_push(to, message):
    # Mock push logic; real one would talk to Firebase or OneSignal
    print(f"[PUSH] To: {to} | Message: {message}")
    return {"status": "sent", "method": "push"}
