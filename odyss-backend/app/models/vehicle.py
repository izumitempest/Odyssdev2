# app/models/vehicle.py
from app.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("companies.id"))
    type = db.Column(db.String(50))
    capacity = db.Column(db.Integer)
    features = db.Column(db.Text)
