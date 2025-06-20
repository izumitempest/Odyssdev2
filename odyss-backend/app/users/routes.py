# routes.py
# app/users/routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity
from app.auth.guards import jwt_required_guard
from app.models.user import User

user_bp = Blueprint("users", __name__, url_prefix="/users")

@user_bp.route("/me", methods=["GET"])
@jwt_required_guard
def get_my_profile():
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "avatar": user.avatar,
        "created_at": user.created_at.isoformat()
    }), 200
