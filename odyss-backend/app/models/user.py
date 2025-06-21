# user.py
# app/models/user.py
from app.extensions import db
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # null if OAuth-only
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # roles = db.relationship("Role", secondary="user_roles", backref="users")


    # OAuth identities
    oauth_identities = relationship("OAuthIdentity", back_populates="user", cascade="all, delete-orphan")
    # Relationships for trips/bookings/payments can go here
    # bookings = db.relationship("Booking", backref="user", lazy=True)
    # trips = db.relationship("Trip", backref="creator", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"
