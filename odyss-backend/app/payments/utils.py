# utils.py
import requests
from flask import current_app

def verify_paystack_payment(reference: str) -> dict:
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to verify payment with Paystack")

    data = response.json()
    if not data['status'] or data['data']['status'] != 'success':
        raise Exception("Payment not successful")

    return data['data']  # return useful info like amount, customer, etc.
