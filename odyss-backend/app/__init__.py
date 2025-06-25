# __init__.py
from flask import Flask
from app.config import Config
from app.extensions import db, jwt, migrate, cors
from app.auth.routes import auth_bp
from app.users.routes import user_bp
from app.trips.routes import trips_bp
from app.bookings.routes import bookings_bp, booking_bp
from app.company.routes import company_bp
from app.payments.routes import payments_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(payments_bp)

    # Register extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    return app
