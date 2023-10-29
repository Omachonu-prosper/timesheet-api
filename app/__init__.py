# External libraries and dependencies
import os
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_cors import CORS
from .reports import reports
from .auth import auth
from .main import main
from .error_handler import error_handler
from .users import users_bp

# Load all environment variables
load_dotenv()

def create_app():
    # def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'SECRET')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(weeks=1)
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

    # Handle CORS
    CORS(app)

    # Bcrypt instantiation
    Bcrypt(app)

    # JWT instantiation 
    JWTManager(app)

    # Register error handlers
    error_handler(app)

    with app.app_context():
        app.register_blueprint(reports)
        app.register_blueprint(auth)
        app.register_blueprint(main)
        app.register_blueprint(users_bp)

        return app