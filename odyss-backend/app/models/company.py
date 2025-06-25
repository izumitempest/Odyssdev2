from app.extensions import db
from uuid import uuid4
from datetime import datetime

class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Uuid, primary_key=True, default=uuid4)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    company_name = db.Column(db.String(120), nullable=False)
    company_email = db.Column(db.String(120), nullable=False)
    company_cert = db.Column(db.Text, nullable=False)  # Base64 encoded image
    access_code = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vehicles = db.relationship("Vehicle", backref="company", lazy=True)
    routes = db.relationship("Route", backref="company", lazy=True)
    payments = db.relationship("CompanyPayment", back_populates="company", lazy=True)
