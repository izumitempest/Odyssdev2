from app.extensions import db
import uuid
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    trip_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('trips.id'), nullable=False)
    seat_number = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, paid, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
