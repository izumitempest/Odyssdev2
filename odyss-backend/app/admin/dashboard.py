# dashboard.py
# app/admin/dashboard.py
from flask import Blueprint, jsonify
from app.models.company import Company
from app.models.trip import Trip
from app.models.booking import Booking
from app.models.user import User
from app.extensions import db
from app.utils.decorators import role_required

admin_dashboard_bp = Blueprint("admin_dashboard", __name__, url_prefix="/admin")

@admin_dashboard_bp.route("/dashboard", methods=["GET"])
@role_required("admin")
def get_admin_dashboard():
    total_users = db.session.query(User).count()
    total_companies = db.session.query(Company).count()
    total_trips = db.session.query(Trip).count()
    total_bookings = db.session.query(Booking).count()

    return jsonify({
        "total_users": total_users,
        "total_companies": total_companies,
        "total_trips": total_trips,
        "total_bookings": total_bookings
    })
