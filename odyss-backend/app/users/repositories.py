# repositories.py
from app.models.user import User
from app.extensions import db

def get_user_by_id(user_id):
    return db.session.get(User, user_id)
