# app/users/routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.user import User
from app.extensions import db

user_bp = Blueprint("users", __name__, url_prefix="/users")

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_profile():
    user_id = get_jwt_identity()     # UUID from identity
    email = get_jwt().get("email")   # Email from additional_claims

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": email,
        "name": user.name,
        "avatar": user.avatar,
        "created_at": user.created_at.isoformat()
    }), 200

@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_my_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    name = data.get("name")
    avatar = data.get("avatar")

    if name:
        user.name = name
    if avatar:
        user.avatar = avatar

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "avatar": user.avatar,
            "created_at": user.created_at.isoformat()
        }
    }), 200
