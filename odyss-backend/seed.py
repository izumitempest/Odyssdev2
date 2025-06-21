
from app.models.user import User
from app.extensions import db
import uuid
from datetime import datetime

# Create a sample user
user = User(
    id=uuid.uuid4(),
    email="izumi@test.com",
    password_hash="not_really_hashed",  # replace with real hash if needed
    name="Izumi the Hacker",
    avatar=None,
    created_at=datetime.utcnow()
)

db.session.add(user)
db.session.commit()
