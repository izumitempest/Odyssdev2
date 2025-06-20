# app/api/v1/routes.py
from flask import Blueprint
from app.auth.routes import auth_bp
from app.users.routes import user_bp
from app.trips.routes import trips_bp

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(user_bp, url_prefix="/users")
api_bp.register_blueprint(trips_bp, url_prefix="/trips")
