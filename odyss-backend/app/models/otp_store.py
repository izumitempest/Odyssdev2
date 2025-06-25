from datetime import datetime
import uuid
from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
class EmailOTP(db.Model):
    __tablename__ = "email_otps"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    data = db.Column(db.JSON, nullable=False)  # Temp store registration payload
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
