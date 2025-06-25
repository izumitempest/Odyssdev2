# app/models/blacklist.py
from app.extensions import db
from datetime import datetime
import uuid

class TokenBlacklist(db.Model):
    __tablename__ = "token_blacklist"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jti = db.Column(db.String(36), nullable=False, unique=True)  # JWT ID
    token_type = db.Column(db.String(10), nullable=False)  # e.g., "refresh"
    user_id = db.Column(db.UUID(as_uuid=True), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    