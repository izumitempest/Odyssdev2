# models.py
# app/auth/models.py
from app.extensions import db
import uuid

class OAuthIdentity(db.Model):
    __tablename__ = 'oauth_identities'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = db.Column(db.String(50), nullable=False)  # e.g., 'google'
    provider_user_id = db.Column(db.String(255), nullable=False)  # e.g., Google sub
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", back_populates="oauth_identities", lazy=True)
