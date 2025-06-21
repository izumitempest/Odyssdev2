from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from app.extensions import db
from app.models.trip import Trip

trips_bp = Blueprint("trips", __name__, url_prefix="/trips")


@trips_bp.route("/", methods=["GET"])
def list_trips():
    trips = Trip.query.all()
    return jsonify({
        "trips": [{
            "id": trip.id,
            "origin": trip.origin,
            "destination": trip.destination,
            "departure_time": trip.departure_time.isoformat(),
            "arrival_time": trip.arrival_time.isoformat() if trip.arrival_time else None,
            "seats_total": trip.seats_total,
            "seats_available": trip.seats_available,
            "price": trip.price
        } for trip in trips],
        "pagination": {
            "page": 1,
            "total": len(trips),
            "pages": 1
        }
    }), 200


@trips_bp.route("/", methods=["POST"])
@jwt_required()
def create_trip():
    data = request.get_json()

    origin = data.get("origin")
    destination = data.get("destination")
    departure_time = data.get("departure_time")
    arrival_time = data.get("arrival_time")
    seats_total = data.get("seats_total")
    price = data.get("price")

    if not all([origin, destination, departure_time, seats_total, price]):
        return jsonify({"error": "Missing required fields."}), 400

    try:
        trip = Trip(
            origin=origin,
            destination=destination,
            departure_time=datetime.fromisoformat(departure_time),
            arrival_time=datetime.fromisoformat(arrival_time) if arrival_time else None,
            seats_total=seats_total,
            seats_available=seats_total,
            price=price
        )
        db.session.add(trip)
        db.session.commit()

        return jsonify({
            "message": "Trip created successfully",
            "trip": {
                "id": trip.id,
                "origin": trip.origin,
                "destination": trip.destination,
                "departure_time": trip.departure_time.isoformat(),
                "arrival_time": trip.arrival_time.isoformat() if trip.arrival_time else None,
                "seats_total": trip.seats_total,
                "seats_available": trip.seats_available,
                "price": trip.price
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import abort

@trips_bp.route("/<trip_id>", methods=["GET"])
def get_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    return jsonify({
        "id": trip.id,
        "origin": trip.origin,
        "destination": trip.destination,
        "departure_time": trip.departure_time.isoformat(),
        "arrival_time": trip.arrival_time.isoformat() if trip.arrival_time else None,
        "seats_total": trip.seats_total,
        "seats_available": trip.seats_available,
        "price": trip.price
    }), 200
