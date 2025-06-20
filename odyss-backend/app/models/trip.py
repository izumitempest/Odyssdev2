# trip.py
# app/models/trip.py

import uuid
from datetime import datetime
from app.extensions import db

class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    origin = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=True)
    seats_total = db.Column(db.Integer, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Trip {self.origin} ➡ {self.destination} | {self.departure_time}>"
