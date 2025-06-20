# __init__.py
from flask import Flask
from app.config import Config
from app.extensions import db, jwt, migrate, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Blueprints here
    # from app.api.v1.routes import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app
