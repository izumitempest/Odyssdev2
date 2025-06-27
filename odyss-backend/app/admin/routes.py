# routes.py
# app/admin/routes.py
from app.admin.dashboard import admin_dashboard_bp

def register_admin_routes(app):
    app.register_blueprint(admin_dashboard_bp)
