# app/models/route.py
from app.extensions import db
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID
class Route(db.Model):
    __tablename__ = "routes"
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("companies.id"), nullable=False)
    origin = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    dep_time = db.Column(db.DateTime)
    price = db.Column(db.Float)
    terminal = db.Column(db.JSON)
    vehicles = db.Column(db.JSON)
