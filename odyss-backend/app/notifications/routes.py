# routes.py
# notifications/routes.py

from flask import Blueprint, request, jsonify
from app.utils.decorators import role_required
from .services import send_notification

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("/send", methods=["POST"])
@role_required("admin")  # or whatever role is allowed to send notifs
def send_notif():
    data = request.get_json()
    
    notif_type = data.get("type")
    recipient = data.get("to")
    subject = data.get("subject", "")
    message = data.get("message")

    if not notif_type or not recipient or not message:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = send_notification(notif_type, recipient, subject, message)
        return jsonify({
            "message": "Notification sent successfully",
            "result": result
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to send notification"}), 500
