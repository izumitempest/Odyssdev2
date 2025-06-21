# repositories.py
from app.models.booking import Booking
from app.extensions import db

def get_passengers_by_trip(trip_id):
    return (
        db.session.query(Booking)
        .filter(Booking.trip_id == trip_id)
        .all()
    )
