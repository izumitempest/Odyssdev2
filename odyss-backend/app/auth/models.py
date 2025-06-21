import uuid  # if not already imported
from app.extensions import db
from sqlalchemy.orm import relationship

class OAuthIdentity(db.Model):
    __tablename__ = 'oauth_identities'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    provider = db.Column(db.String(50), nullable=False)
    provider_user_id = db.Column(db.String(120), nullable=False)
    access_token = db.Column(db.String, nullable=True)
    user = relationship("User", back_populates="oauth_identities")
