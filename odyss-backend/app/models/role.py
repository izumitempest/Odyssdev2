import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationship: one role has many users
    users = db.relationship("User", back_populates="role", lazy="dynamic")

    def __repr__(self):
        return f"<Role {self.name}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name
        }
