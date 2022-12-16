"""Initialize app."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    
    # WEBSITE_HOSTNAME exists only in production environment
    if not 'WEBSITE_HOSTNAME' in os.environ:
        # local development, where we'll use environment variables
        app.config.from_object('azureproject.development')
    else:
        # production
        print("Loading config.production.")
        app.config.from_object('azureproject.production')

        app.config.update(
            SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import auth, routes
        from .assets import compile_static_assets

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()

        # Compile static assets
        if app.config["FLASK_ENV"] == "development":
            compile_static_assets(app)
        return app
