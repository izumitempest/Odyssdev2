# payment.py
import uuid
from datetime import datetime
from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    booking_id = db.Column(UUID(as_uuid=True), db.ForeignKey("bookings.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="NGN")
    payment_method = db.Column(db.String(20))  # e.g., "paystack", "flutterwave"
    status = db.Column(db.String(20), default="pending")  # pending, successful, failed
    reference = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Payment {self.reference} | ₦{self.amount} | {self.status}>"
    

class CompanyPayment(db.Model):
    __tablename__ = "payments_company"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("companies.id"))
    company = db.relationship("Company", back_populates="payments")

