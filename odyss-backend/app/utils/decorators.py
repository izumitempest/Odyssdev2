from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify

def role_required(role_name):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != role_name:
                return jsonify({"error": "Access forbidden: Requires {} role".format(role_name)}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


