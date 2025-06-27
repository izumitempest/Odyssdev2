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
    "id": str(user.id),
    "email": email,
    "name": user.name,
    "first_name": user.first_name,
    "last_name": user.last_name,
    "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
    "vibes": user.vibes if user.vibes else [],
    "nickname": user.name,
    "bio": user.bio,
    "phone_number": user.phone_number,
    "avatar": user.avatar,
    "intro_video": user.intro_video,
    "role": user.role.name if user.role else None,
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

    if "name" in data:
        user.name = data["name"]
    if "avatar" in data:
        user.avatar = data["avatar"]
    if "bio" in data:
        user.bio = data["bio"]
    if "intro_video" in data:
        user.intro_video = data["intro_video"]
    if "phone_number" in data:
        user.phone_number = data["phone_number"]

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "user": {
            "email": user.email,
            "name": user.name,
            "id": user.id,
            "avatar": user.avatar,
            "created_at": user.created_at.isoformat(),
            "phone_number": user.phone_number,
            "bio": user.bio,
            "intro_video": user.intro_video,
            "role": user.role.name if user.role else None,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
            "vibes": user.vibes if user.vibes else [],
            "nickname": user.name
        }
    }), 200
