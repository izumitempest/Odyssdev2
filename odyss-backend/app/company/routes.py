# app/company/routes.py

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.company import Company
from app.models.route import Route
from app.models.vehicle import Vehicle
from app.models.company_trip import CompanyTrip
from app.utils.decorators import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import json
import os
from app.auth.utils import hash_password, verify_password
from flask_jwt_extended import create_access_token, create_refresh_token
import datetime
from app.models.company import Company
from werkzeug.security import check_password_hash
from sqlalchemy.orm import joinedload
from app.models.booking import Booking
from app.models.company_trip import CompanyTrip
from app.models.user import User


# -*- coding: utf-8 -*-
# app/company/routes.py


company_bp = Blueprint("company", __name__, url_prefix="/company")


@company_bp.route("/signup", methods=["POST"])
def company_signup():
    data = request.get_json()

    required_fields = [
        "name", "email", "password", "company_name",
        "company_email", "company_cert", "accessCode"
    ]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if Company.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    if data["accessCode"] != os.getenv("COMPANY_ACCESS_CODE"):
        return jsonify({"error": "Invalid access code"}), 403

    new_company = Company(
        name=data["name"],
        email=data["email"],
        password_hash=hash_password(data["password"]),
        company_name=data["company_name"],
        company_email=data["company_email"],
        company_cert=data["company_cert"],
        access_code=data["accessCode"]
    )

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "Company account created successfully", "company_id": new_company.id}), 201

@company_bp.route("/login", methods=["POST"])
def company_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    company = Company.query.filter_by(email=email).first()

    if not company or not check_password_hash(company.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(company.id),
        additional_claims={"role": "company", "email": company.email},
        expires_delta=datetime.timedelta(seconds)
    )
    refresh_token = create_refresh_token(identity=str(company.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "company_id": str(company.id),
        "company_name": company.company_name
    }), 200

@company_bp.route("/me", methods=["GET"])
@jwt_required()
def get_company_profile():
    claims = get_jwt()
    role = claims.get("role")

    if role != "company":
        return jsonify({"error": "Access denied"}), 403

    company_id = get_jwt_identity()
    company = Company.query.get(company_id)

    if not company:
        return jsonify({"error": "Company not found"}), 404

    return jsonify({
        "id": str(company.id),
        "name": company.name,
        "email": company.email,
        "company_name": company.company_name,
        "company_email": company.company_email,
        "company_cert": company.company_cert,
        "created_at": company.created_at.isoformat()
    }), 200



@company_bp.route("/trips", methods=["POST"])
@jwt_required()
@role_required("company")
def create_trip():
    data = request.get_json()
    route_id = data.get("route_id")
    departure_time = data.get("departure_time")
    arrival_time = data.get("arrival_time")
    seats_total = data.get("seats_total")
    price = data.get("price")

    if not all([route_id, departure_time, arrival_time, seats_total, price]):
        return jsonify({"error": "Missing required fields"}), 400

    route = Route.query.get(route_id)
    if not route:
        return jsonify({"error": "Route not found"}), 404

    trip = CompanyTrip(
        route_id=route.id,
        departure_time=departure_time,
        arrival_time=arrival_time,
        seats_total=seats_total,
        seats_available=seats_total,
        price=price
    )
    db.session.add(trip)
    db.session.commit()

    return jsonify({"message": "Trip created successfully", "trip_id": trip.id}), 201


from app.models.vehicle import Vehicle

@company_bp.route("/vehicles", methods=["POST"])
@jwt_required()
@role_required("company")
def add_vehicle():
    data = request.get_json()
    vehicle_type = data.get("type")
    capacity = data.get("capacity")
    features = data.get("features")  # Optional, e.g. "AC, WiFi, Charging"

    if not all([vehicle_type, capacity]):
        return jsonify({"error": "Vehicle type and capacity required"}), 400

    company_id = get_jwt_identity()

    vehicle = Vehicle(
        company_id=company_id,
        type=vehicle_type,
        capacity=capacity,
        features=features
    )

    db.session.add(vehicle)
    db.session.commit()

    return jsonify({"message": "Vehicle added successfully", "vehicle_id": vehicle.id}), 201



@company_bp.route("/routes", methods=["POST"])
@jwt_required()
@role_required("company")
def create_route():
    data = request.get_json()
    origin = data.get("origin")
    destination = data.get("destination")
    dep_time = data.get("dep_time")
    price = data.get("price")
    terminal = data.get("terminal")  # Should be JSON
    vehicles = data.get("vehicles")  # Should be list or JSON

    if not all([origin, destination, dep_time, price, terminal, vehicles]):
        return jsonify({"error": "Missing required fields"}), 400

    company_id = get_jwt_identity()

    route = Route(
        company_id=company_id,
        origin=origin,
        destination=destination,
        dep_time=dep_time,
        price=price,
        terminal=terminal,
        vehicles=vehicles
    )

    db.session.add(route)
    db.session.commit()

    return jsonify({"message": "Route created successfully", "route_id": route.id}), 201

# app/company/routes.py

@company_bp.route("/trips", methods=["GET"])
@jwt_required()
@role_required("company")
def list_company_trips():
    company_id = get_jwt_identity()

    # Get all routes owned by this company
    routes = Route.query.filter_by(company_id=company_id).all()
    route_ids = [r.id for r in routes]

    # Get all trips tied to those routes
    trips = CompanyTrip.query.filter(CompanyTrip.route_id.in_(route_ids)).all()

    result = []
    for trip in trips:
        route = Route.query.get(trip.route_id)
        if route:
            route_info = {
                "origin": route.origin,
                "destination": route.destination
            }
        else:
            route_info = {
                "origin": None,
                "destination": None
            }
        result.append({
            "trip_id": str(trip.id),
            "route": route_info,
            "departure_time": trip.departure_time.isoformat(),
            "arrival_time": trip.arrival_time.isoformat() if trip.arrival_time else None,
            "seats_total": trip.seats_total,
            "seats_available": trip.seats_available,
            "price": trip.price
        })

    return jsonify(result), 200

@company_bp.route("/trips/<uuid:trip_id>", methods=["PATCH"])
@jwt_required()
@role_required("company")
def update_trip(trip_id):
    data = request.get_json()
    trip = CompanyTrip.query.get_or_404(trip_id)

    # Optional fields
    trip.departure_time = data.get("departure_time", trip.departure_time)
    trip.arrival_time = data.get("arrival_time", trip.arrival_time)
    trip.price = data.get("price", trip.price)
    trip.seats_total = data.get("seats_total", trip.seats_total)
    
    # Update available seats if seats_total changed
    if "seats_total" in data:
        difference = data["seats_total"] - trip.seats_total
        trip.seats_available += difference

    db.session.commit()

    return jsonify({"message": "Trip updated successfully", "trip_id": str(trip.id)}), 200

@company_bp.route("/trips/<trip_id>", methods=["DELETE"])
@jwt_required()
@role_required("company")
def delete_trip(trip_id):
    company_id = get_jwt_identity()
    trip = CompanyTrip.query.options(joinedload(CompanyTrip.route)).filter_by(id=trip_id).first()

    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    print(f"Trip route company: {trip.route.company_id}, Current company: {company_id}")
    print("Trip route company:", trip.route.company_id)
    print("Current company:", company_id)
    print("Route:", trip.route)
    print("Trip object:", trip)


    # if trip.route.company_id != company_id:
    #     return jsonify({"error": "Unauthorized to delete this trip"}), 403
    if str(trip.route.company_id) != str(company_id):
        print("Unauthorized: mismatch after str casting.")
        return jsonify({"error": "Unauthorized to delete this trip"}), 403


    db.session.delete(trip)
    db.session.commit()
    
    return jsonify({
        "message": "Trip deleted successfully",
        "trip_id": trip_id
    }), 200

@company_bp.route("/bookings", methods=["GET"])
@jwt_required()
@role_required("company")
def get_all_company_bookings():
    current_company_id = get_jwt_identity()
    
    bookings = (
    db.session.query(Booking)
    .join(CompanyTrip, Booking.trip_id == CompanyTrip.id)
    .join(Route, CompanyTrip.route_id == Route.id)
    .join(User, Booking.user_id == User.id)
    .filter(Route.company_id == current_company_id)
    .all()
)


    result = []
    for booking in bookings:
        result.append({
            "booking_id": str(booking.id),
            "user": {
                "id": str(booking.user.id),
                "name": booking.user.name,
                "email": booking.user.email
            },
            "trip": {
                "id": str(booking.trip.id),
                "origin": booking.trip.route.origin,
                "destination": booking.trip.route.destination,
                "departure_time": booking.trip.departure_time.isoformat()
            },
            "seat_number": booking.seat_number,
            "status": booking.status,
            "created_at": booking.created_at.isoformat()
        })

    return jsonify(result), 200



