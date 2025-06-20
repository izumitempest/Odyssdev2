# routes.py
from flask import Blueprint, jsonify, request
from app.models.trip import Trip

trips_bp = Blueprint("trips", __name__, url_prefix="/trips")

@trips_bp.route("/", methods=["GET"])
def list_trips():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("limit", 10))

    trips = Trip.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "trips": [
            {
                "id": trip.id,
                "origin": trip.origin,
                "destination": trip.destination,
                "departure_time": trip.departure_time.isoformat(),
                "seats_available": trip.seats_available
            } for trip in trips.items
        ],
        "pagination": {
            "page": trips.page,
            "total": trips.total,
            "pages": trips.pages
        }
    }), 200
