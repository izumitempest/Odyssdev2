# services.py
from app.users.repositories import get_user_by_id
from app.bookings.repositories import get_passengers_by_trip

def list_passengers_for_trip(trip_id):
    bookings = get_passengers_by_trip(trip_id)
    passengers = []

    for b in bookings:
        user = get_user_by_id(b.user_id)
        passengers.append({
            "user_id": b.user_id,
            "name": user.name if user else None,
            "seat_number": b.seat_number,
            "status": b.status
        })

    return passengers
