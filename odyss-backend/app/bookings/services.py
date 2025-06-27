# app/bookings/services.py

from uuid import UUID
from datetime import datetime
from typing import List, Optional

from app.extensions import db
from app.models.booking import Booking
from app.models.trip import Trip
from app.models.user import User
from app.core.exceptions import NotFoundException, BadRequestException


def create_booking(user_id: UUID, trip_id: UUID, seat_number: Optional[int] = None) -> Booking:
    trip = Trip.query.get(trip_id)
    if not trip:
        raise NotFoundException("Trip not found")

    taken_seats = get_taken_seats(trip_id)
    if seat_number is not None and seat_number in taken_seats:
        raise BadRequestException("Seat already taken")

    # Default to first available seat if none selected
    if seat_number is None:
        all_seats = list(range(1, trip.capacity + 1))
        available = [seat for seat in all_seats if seat not in taken_seats]
        if not available:
            raise BadRequestException("No seats available")
        seat_number = available[0]

    booking = Booking(
        user_id=user_id,
        trip_id=trip_id,
        seat_number=seat_number,
        status="pending",
        created_at=datetime.utcnow()
    )
    db.session.add(booking)
    db.session.commit()
    return booking


def get_user_bookings(user_id: UUID) -> List[Booking]:
    return Booking.query.filter_by(user_id=user_id).all()


def cancel_booking(booking_id: UUID, user_id: UUID) -> None:
    booking = Booking.query.get(booking_id)
    if not booking:
        raise NotFoundException("Booking not found")
    if booking.user_id != user_id:
        raise BadRequestException("Unauthorized to cancel this booking")

    db.session.delete(booking)
    db.session.commit()


def get_taken_seats(trip_id: UUID) -> List[int]:
    bookings = Booking.query.filter_by(trip_id=trip_id).all()
    return [b.seat_number for b in bookings if b.status != "cancelled"]

# from app.notifications.services import send_notification

# # After booking is created
# send_notification(
#     type="email",  # or "sms"
#     recipient=User.email,
#     subject="Booking Confirmed!",
#     # message=f"Your booking for the trip from {Trip.route.origin} to {Trip.route.destination} has been confirmed."
# )
