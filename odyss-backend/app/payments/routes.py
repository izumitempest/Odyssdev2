# routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.payments.utils import verify_paystack_payment
from app.models.booking import Booking
from app.extensions import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import requests
from app.extensions import db
from app.models.payment import Payment
from app.config import Config
import uuid
from app.models.trip import Trip
from uuid import UUID
import flask_cors
from flask_cors import CORS


payments_bp = Blueprint('payments', __name__, url_prefix='/payments')



@payments_bp.route('/verify', methods=['POST'])
@jwt_required()
def verify_payment():
    data = request.get_json()
    reference = data.get("reference")
    booking_id = data.get("booking_id")
    user_id = get_jwt_identity()

    if not reference or not booking_id:
        return jsonify({"error": "Missing reference or booking ID"}), 400

    
    # Hit Paystack verification API
    headers = {
        "Authorization": f"Bearer {Config.PAYSTACK_SECRET_KEY}"
    }
    response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Verification failed"}), 400

    result = response.json()
    if result['data']['status'] == "success":
        # Mark booking as paid
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        booking.status = "paid"
         # Check if payment already exists
        payment = Payment.query.filter_by(reference=reference).first()
        if payment:
            payment.status = "success"
        else:
            payment = Payment(
                user_id=user_id,
                booking_id=booking_id,
                amount=result["data"]["amount"] / 100,
                currency="NGN",
                payment_method="paystack",
                status="success",
                reference=reference,
            )
            db.session.add(payment)
        db.session.commit()

        return jsonify({"status": "success", "message": "Payment verified and booking updated"}), 200

    return jsonify({"status": "failed", "message": "Payment not successful"}), 400

@payments_bp.route("/history", methods=["GET"])
@jwt_required()
def payment_history():
    user_id = get_jwt_identity()
    bookings = Booking.query.filter_by(user_id=user_id, status="paid").all()
    return jsonify([{
        "booking_id": str(b.id),
        "trip_id": str(b.trip_id),
        "seat_number": b.seat_number,
        "status": b.status,
        "created_at": b.created_at.isoformat()
    } for b in bookings]), 200

@payments_bp.route("/initiate", methods=["POST"])
@jwt_required()
def initiate_payment():
    user_id = get_jwt_identity()
    data = request.get_json()
    booking_id = data.get("booking_id")
    payment_method = data.get("payment_method", "paystack")

    booking = Booking.query.get(booking_id)

    user_id = UUID(get_jwt_identity())
    if not booking or booking.user_id != user_id:
        return jsonify({"error": "Invalid booking"}), 404

    # You can calculate the amount based on trip price or booking data
    trip = Trip.query.get(booking.trip_id)
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    amount = trip.price

    # Generate a unique reference
    reference = f"ODYSS-{uuid.uuid4().hex[:12].upper()}"

    payment = Payment(
        user_id=user_id,
        booking_id=booking_id,
        amount=amount,
        payment_method=payment_method,
        reference=reference,
    )
    db.session.add(payment)
    db.session.commit()

    # Return the reference and amount for frontend to trigger Paystack inline
    return jsonify({
        "message": "Payment initiated",
        "reference": reference,
        "amount": amount,
        "payment_method": payment_method,
        "currency": "NGN"
    }), 200
