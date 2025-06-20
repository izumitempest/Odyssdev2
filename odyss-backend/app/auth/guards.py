# guards.py
# app/auth/guards.py
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from app.models.user import User
# from app.models.role import Role  # Assuming role model exists

def jwt_required_guard(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": "Unauthorized"}), 401
        return fn(*args, **kwargs)
    return wrapper


def role_required(required_roles):
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            user = User.query.get(identity["id"])

            user_roles = [r.name for r in user.roles] if user and hasattr(user, "roles") else []
            if not any(role in user_roles for role in required_roles):
                return jsonify({"error": "Forbidden: insufficient role"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def same_user_or_admin(user_id_key="user_id"):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            jwt_user_id = identity.get("id")
            target_user_id = kwargs.get(user_id_key)

            user = User.query.get(jwt_user_id)
            is_admin = any(r.name == "admin" for r in user.roles) if user else False

            if str(jwt_user_id) != str(target_user_id) and not is_admin:
                return jsonify({"error": "Forbidden: not your resource"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
