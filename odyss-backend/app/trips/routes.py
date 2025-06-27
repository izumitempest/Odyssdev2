from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from app.extensions import db
from app.models.trip import Trip
from sqlalchemy import or_, and_

trips_bp = Blueprint("trips", __name__, url_prefix="/trips")


@trips_bp.route("/", methods=["GET"])
def list_trips():
    trips = Trip.query.all()
    return jsonify({
        "trips": [{
            "id": trip.id,
            "origin": trip.origin,
            "destination": trip.destination,
            "departure_time": trip.departureDate.isoformat(),
            "arrival_time": trip.arrivalDate.isoformat() if trip.arrivalDate else None,
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

    departureLoc = data.get("departureLoc")
    arrivalLoc = data.get("arrivalLoc")
    departureDate = data.get("departureDate")
    arrivalDate = data.get("arrivalDate")
    seats = data.get("seats")
    price = data.get("price")
    vehicle = data.get("vehicle")
    memberIds = data.get("memberIds", [])
    company = data.get("company")
    departureTOD = data.get("departureTOD")
    creator = data.get("creator")
    fill = data.get("fill", False)
    vibes = data.get("vibes", [])

    if not all([departureLoc, arrivalLoc, departureDate, arrivalDate, seats, price, vehicle, memberIds, company, departureTOD, creator, fill, vibes]):
        return jsonify({"error": "Missing required fields."}), 400

    try:
        trip = Trip(
            departureLoc=departureLoc,
            arrivalLoc=arrivalLoc,
            departureDate=datetime.fromisoformat(departureDate),
            arrivalDate=datetime.fromisoformat(arrivalDate) if arrivalDate else None,
            seats=seats,
            price=price,
            vehicle=vehicle,
            memberIds=memberIds,
            company=company,
            departureTOD=departureTOD,
            creator=creator,
            fill=fill,
            vibes=vibes
        )
        db.session.add(trip)
        db.session.commit()

        return jsonify({
            "message": "Trip created successfully",
            "trip": {
            "id": trip.id,
            "departureLoc": trip.departureLoc,
            "arrivalLoc": trip.arrivalLoc,
            "departureDate": trip.departureDate.isoformat() if trip.departureDate else None,
            "arrivalDate": trip.arrivalDate.isoformat() if trip.arrivalDate else None,
            "seats": trip.seats,
            "price": trip.price,
            "vehicle": trip.vehicle,
            "memberIds": trip.memberIds,
            "company": trip.company,
            "departureTOD": trip.departureTOD,
            "creator": trip.creator,
            "fill": trip.fill,
            "vibes": trip.vibes
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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


@trips_bp.route("/search", methods=["GET"])
def search_trips():
    origin = request.args.get("origin", "").lower()
    destination = request.args.get("destination", "").lower()
    date_str = request.args.get("date")  # Expected format: YYYY-MM-DD
    time_str = request.args.get("time")  # Expected format: HH:MM

    query = Trip.query

    # Collect filters and similarity score
    filters = []
    similarity = []

    if origin:
        filters.append(Trip.origin.ilike(f"%{origin}%"))
        similarity.append((Trip.origin.ilike(f"%{origin}%"), 3))
    if destination:
        filters.append(Trip.destination.ilike(f"%{destination}%"))
        similarity.append((Trip.destination.ilike(f"%{destination}%"), 3))
    if date_str:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            filters.append(Trip.departure_date.cast(db.Date) == date)
            similarity.append((Trip.departure_date.cast(db.Date) == date, 2))
        except Exception:
            pass
    if time_str:
        try:
            time = datetime.strptime(time_str, "%H:%M").time()
            filters.append(db.extract('hour', Trip.departure_tod) == time.hour)
            similarity.append((db.extract('hour', Trip.departure_tod) == time.hour, 1))
        except Exception:
            pass

    # Filter trips that match at least one filter
    if filters:
        trips = Trip.query.filter(or_(*filters)).all()
    else:
        trips = Trip.query.all()

    # Score and sort trips by similarity
    def trip_score(trip):
        score = 0
        if origin and origin in trip.origin.lower():
            score += 3
        if destination and destination in trip.destination.lower():
            score += 3
        if date_str and trip.dep_time.date().isoformat() == date_str:
            score += 2
        if time_str and trip.dep_time.strftime("%H:%M") == time_str:
            score += 1
        return score

    trips = sorted(trips, key=trip_score, reverse=True)

    result = [{
        "id": str(trip.id),
        "origin": trip.origin,
        "destination": trip.destination,
        "dep_time": trip.dep_time.isoformat(),
        "price": trip.price,
        "capacity": trip.capacity
    } for trip in trips]

    return jsonify(result), 200
