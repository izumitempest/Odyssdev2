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
        tokens = generate_tokens(user)  # ✅ user is the full SQLAlchemy object

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

    tokens = generate_tokens(user)  # ✅ user is the full SQLAlchemy object

    return jsonify(tokens), 200




@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # In stateless JWT, logout is typically handled client-side
    # But you can implement token blacklisting if needed
    return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.route("/request-otp", methods=["POST"])
def request_otp():
    data = request.get_json()
    email = data.get("email")
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # TODO: Implement OTP generation and sending logic
    # For now, return success
    return jsonify({"message": "OTP sent successfully"}), 200


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    
    # TODO: Implement OTP verification logic
    # For now, return success for demonstration
    return jsonify({"message": "OTP verified successfully"}), 200


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("new_password")
    otp = data.get("otp")  # or token
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # TODO: Verify OTP/token before resetting
    user.password_hash = hash_password(new_password)
    db.session.commit()
    
    return jsonify({"message": "Password reset successfully"}), 200

# Fix the refresh token route
