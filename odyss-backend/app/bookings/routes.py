from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.booking import Booking
from app.auth.guards import admin_required, driver_required
from app.bookings.repositories import get_passengers_by_trip as list_passengers_for_trip

from app.models.trip import Trip
from datetime import datetime
import uuid

bookings_bp = Blueprint("bookings", __name__, url_prefix="/trips")
booking_bp = Blueprint("booking_routes", __name__, url_prefix="/bookings")


@bookings_bp.route("/<trip_id>/book", methods=["POST"])
@jwt_required()
def book_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    if trip.seats_available <= 0:
        return jsonify({"error": "No seats available"}), 400

    user_id = get_jwt_identity()

    # Check if user already booked this trip (optional)
    existing_booking = Booking.query.filter_by(user_id=user_id, trip_id=trip_id).first()
    if existing_booking:
        return jsonify({"error": "Already booked this trip"}), 409

    # Create booking
    booking = Booking(
        id=str(uuid.uuid4()),
        user_id=user_id,
        trip_id=trip_id,
        created_at=datetime.utcnow()
    )

    trip.seats_available -= 1
    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "Booking successful",
        "booking": {
            "id": booking.id,
            "trip_id": trip.id,
            "user_id": booking.user_id,
            "created_at": booking.created_at.isoformat()
        }
    }), 201

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.booking import Booking
from app.models.trip import Trip

@booking_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_bookings():
    user_id = get_jwt_identity()

    bookings = (
        db.session.query(Booking, Trip)
        .join(Trip, Booking.trip_id == Trip.id)
        .filter(Booking.user_id == user_id)
        .all()
    )

    return jsonify([
        {
            "booking_id": str(booking.id),
            "trip_id": str(trip.id),
            "origin": trip.origin,
            "destination": trip.destination,
            "departure_time": trip.departure_time.isoformat(),
            "arrival_time": trip.arrival_time.isoformat(),
            "created_at": booking.created_at.isoformat()
        }
        for booking, trip in bookings
    ])

@booking_bp.route('/<uuid:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    user_id = get_jwt_identity()
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()

    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    # Increase trip's available seats
    trip = Trip.query.get(booking.trip_id)
    if trip:
        trip.seats_available += 1

    db.session.delete(booking)
    db.session.commit()

    return jsonify({'message': 'Booking canceled successfully'})

@booking_bp.route("/trips/<uuid:trip_id>/passengers", methods=["GET"])
@jwt_required()
@admin_required  # or replace with @driver_required if needed
def get_trip_passengers(trip_id):
    passengers = list_passengers_for_trip(trip_id)
    return jsonify(passengers), 200


