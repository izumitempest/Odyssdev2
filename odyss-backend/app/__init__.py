# __init__.py
from flask import Flask
from app.config import Config
from app.extensions import db, jwt, migrate, cors
from app.auth.routes import auth_bp
from app.users.routes import user_bp
from app.trips.routes import trips_bp
# from .api.v1.routes import api_bp
from app.bookings.routes import bookings_bp
from app.bookings.routes import booking_bp
from app.payments.routes import payments_bp
from flask_cors import CORS




def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(payments_bp)
    

    @app.after_request
    def apply_cors(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response


    # Register API Blueprint
    # app.register_blueprint(api_bp, url_prefix='/api/v1')


    # Register extensions

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Blueprints here
    # from app.api.v1.routes import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app
