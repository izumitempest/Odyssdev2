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
from app.models.role import Role
from app.models.email_otp import EmailOTP
from app.auth.utils import send_otp_email
from werkzeug.security import generate_password_hash
from app.utils.otp import generate_otp
from datetime import datetime, timedelta, timezone
import re
from flask import request, jsonify
from app.services.otp_service import generate_and_store_otp
from app.utils.email_sender import send_otp_email
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.models.role import Role
from app.models.email_otp import EmailOTP
from app.extensions import db
from flask import request, jsonify
# In-memory store for OTPs (for development/testing only)


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
        default_role = Role.query.filter_by(name="user").first()


        if not user:
            user = User(email=email, name=name, avatar=avatar)
            user.role = default_role
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
        tokens = generate_tokens(user)  # user is the full SQLAlchemy object

        return jsonify(tokens), 200

    except Exception as e:
        print("OAuth error:", e)
        return jsonify({"error": "Invalid token"}), 400
    

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")


    if not email or not otp:
        return jsonify({"error": "Email and OTP are required"}), 400


    record = EmailOTP.query.filter_by(email=email).first()
    if not record or record.otp != otp:
        return jsonify({"error": "Invalid OTP"}), 400
    if record.is_expired():
        return jsonify({"error": "OTP expired"}), 400

    # OTP valid: mark user as verified or allow account creation
    db.session.delete(record)  # optional: remove OTP after success
    db.session.commit()

    return jsonify({"message": "OTP verified"}), 200


@auth_bp.route('/request-otp', methods=['POST'])
def request_otp():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Valid email is required"}), 400

    otp = generate_and_store_otp(email)

    print(f"📨 Sending OTP {otp} to {email}...")

    if not send_otp_email(email, otp):
        return jsonify({"error": "Failed to send OTP email"}), 500

    return jsonify({"message": "OTP sent successfully"}), 200



@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    required_fields = ["first_name", "last_name", "nickname", "email", "password", "bio", "phone_number", "profile_pic", "intro_video"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    email = data["email"]

    # Check OTP (must NOT exist if deleted on verification)
    if EmailOTP.query.filter_by(email=email).first():
        return jsonify({"error": "Email not verified"}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    # Fetch or create the default "user" role
    role = Role.query.filter_by(name="user").first()
    if not role:
        role = Role(name="user")
        db.session.add(role)
        db.session.commit()

    # Create new user (correctly map fields to model)
    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        name=data["nickname"],
        email=email,
        password_hash=generate_password_hash(data["password"]),
        bio=data["bio"],
        phone_number=data["phone_number"],
        avatar=data["profile_pic"],
        intro_video=data["intro_video"],
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

    # user.role = default_role  # Assign the default role
    # db.session.add(user)
    # db.session.commit()

    # return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    
    if not user or not verify_password(password, user.password_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    tokens = generate_tokens(user)  # typically returns { access, refresh }

    return jsonify({
        "message": "Login successful",
        "tokens": tokens,
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role.name if user.role else "user",
            "avatar": user.avatar
        }
    }), 200

@auth_bp.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    tokens = generate_tokens(user)
    return jsonify(tokens), 200