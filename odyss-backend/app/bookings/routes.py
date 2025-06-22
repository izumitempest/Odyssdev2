from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.booking import Booking
from app.auth.guards import admin_required, driver_required
from app.bookings.repositories import get_passengers_by_trip as list_passengers_for_trip
from app.bookings.services import create_booking, get_taken_seats
from app.bookings.schemas import BookingRequestSchema
from marshmallow import ValidationError

from app.models.trip import Trip

bookings_bp = Blueprint("bookings", __name__, url_prefix="/trips")
booking_bp = Blueprint("booking", __name__, url_prefix="/bookings")


@bookings_bp.route('/<uuid:trip_id>/book', methods=['POST'])
@jwt_required()
def book_trip(trip_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    try:
        validated = BookingRequestSchema().load(data)
        booking = create_booking(user_id, trip_id, validated['seat_number'])
        trip = Trip.query.get(trip_id)
        if trip is None:
            return jsonify({"error": "Trip not found"}), 404
        if trip.seats_available <= 0:
            return jsonify({"error": "No seats available for this trip"}), 400
        trip.seats_available -= 1
        db.session.commit()
        db.session.refresh(booking)
        db.session.refresh(trip)
        return jsonify({
            "message": "Booking successful",
            "booking": {
                "id": str(booking.id),
                "seat_number": booking.seat_number,
                "status": booking.status
            }
        }), 201
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400


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


@booking_bp.route("/<uuid:trip_id>/passengers", methods=["GET"])
@jwt_required()
@admin_required  # or replace with @driver_required if needed
def get_trip_passengers(trip_id):
    passengers = list_passengers_for_trip(trip_id)
    return jsonify(passengers), 200


@bookings_bp.route('/<uuid:trip_id>/seats', methods=['GET'])
@jwt_required()
def get_trip_seats(trip_id):
    seats = get_taken_seats(trip_id)
    return jsonify({
        "trip_id": str(trip_id),
        "seats_taken": seats
    })