# routes.py
# app/auth/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.auth.models import OAuthIdentity
from app.auth.utils import hash_password, verify_password, generate_tokens
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/oauth/google", methods=["POST"])
def google_oauth():
    data = request.get_json()
    token = data.get("id_token")

    try:
        # Verify token with Google
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(),
            audience=None  # Can hardcode client ID for strict check
        )

        email = idinfo.get("email")
        name = idinfo.get("name")
        avatar = idinfo.get("picture")
        provider_user_id = idinfo.get("sub")

        # Check if user exists
        user = User.query.filter_by(email=email).first()

        if not user:
            user = User(email=email, name=name, avatar=avatar)
            db.session.add(user)
            db.session.flush()  # get user.id

        # Check or create OAuth identity
        identity = OAuthIdentity.query.filter_by(
            provider='google', provider_user_id=provider_user_id
        ).first()

        if not identity:
            identity = OAuthIdentity(
                provider="google",
                provider_user_id=provider_user_id,
                user_id=user.id
            )
            db.session.add(identity)

        db.session.commit()

        tokens = generate_tokens({"id": user.id, "email": user.email})
        return jsonify(tokens), 200

    except Exception as e:
        print("OAuth error:", e)
        return jsonify({"error": "Invalid token"}), 400


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(email=email, password_hash=hash_password(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    tokens = generate_tokens({"id": user.id, "email": user.email})
    return jsonify(tokens), 200


@auth_bp.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    new_token = generate_tokens(identity)
    return jsonify(new_token), 200
