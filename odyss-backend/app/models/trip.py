# trip.py
# app/models/trip.py
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.extensions import db

class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # seats_total = db.Column(db.Integer, nullable=False)
    # seats_available = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False)  # Total seats available for the trip
    price = db.Column(db.Float, nullable=False)
    # transport_partner = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), default="active")  # e.g., "active", "cancelled", "completed"
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    vehicle = db.Column(db.String(120), nullable=False)
    memberIds = db.Column(db.ARRAY(db.String), nullable=False)  # or JSON if using SQLite
    company = db.Column(db.String(120), nullable=False)  # Company name if applicable
    departureLoc = db.Column(db.String(120), nullable=False)
    arrivalLoc = db.Column(db.String(120), nullable=False)
    departureTOD = db.Column(db.String(100), nullable=False)  # Time of day as string, e.g. "09:00"
    departureDate = db.Column(db.DateTime, nullable=False)
    arrivalDate = db.Column(db.DateTime, nullable=False)
    creator = db.Column(db.String(120), nullable=False)
    fill = db.Column(db.Boolean, default=False)
    vibes = db.Column(db.ARRAY(db.String), nullable=False)  # List of vibes or tags associated with the trip

    def __repr__(self):
        return f"<Trip {self.departureLoc} ➡ {self.arrivalLoc} | {self.departureDate} {self.departureTOD}>"
