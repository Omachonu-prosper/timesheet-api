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

# Load all environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'SECRET')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(weeks=1)
    app.register_blueprint(reports)
    app.register_blueprint(auth)
    app.register_blueprint(main)

    # Handle CORS
    CORS(app)

    # Bcrypt instantiation
    Bcrypt(app)

    # JWT instantiation 
    JWTManager(app)

    # Register error handlers
    error_handler(app)
    
    return app