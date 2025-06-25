# services.py
from app.extensions import db
from app.models.user import User
from app.models.role import Role

default_role = Role.query.filter_by(name="user").first()
new_user.role = default_role
