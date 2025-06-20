# role.py
# app/models/role.py or wherever shared
from app.extensions import db

user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.String, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)
