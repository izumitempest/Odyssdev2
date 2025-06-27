# trip.py
# app/models/trip.py
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.extensions import db

class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=True)
    seats_total = db.Column(db.Integer, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    transport_partner = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), default="active")  # e.g., "active", "cancelled", "completed"
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Trip {self.origin} ➡ {self.destination} | {self.departure_time}>"
