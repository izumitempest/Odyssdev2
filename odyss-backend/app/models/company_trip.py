# app/models/company_trip.py
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.extensions import db
from app.models.route import Route  # Assuming Route model is defined in route.py
# app/models/company_trip.py
class CompanyTrip(db.Model):
    __tablename__ = "company_trips"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    route_id = db.Column(UUID(as_uuid=True), db.ForeignKey("routes.id"), nullable=False)
    route = db.relationship("Route", backref="company_trips")

    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=True)

    seats_total = db.Column(db.Integer, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)

    price = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<CompanyTrip route={self.route_id} dt={self.departure_time}>"
