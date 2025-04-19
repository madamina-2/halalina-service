from flask import Flask
from app.models.job_type import JobType
from config import Config
from app.models import db
from app.controllers import auth_bp, user_profile_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


def create_app():
    """Factory function to create and configure the Flask app."""
    
    # Create a Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)

    # Initialize database (SQLAlchemy)
    db.init_app(app)
    Migrate(app, db)

    # Initialize JWT manager for handling tokens
    JWTManager(app)
    
    # Set up CORS based on environment configuration
    init_cors(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register auth routes
    app.register_blueprint(user_profile_bp, url_prefix='/user_profile')  # Register user profile routes

    # Inisialisasi database dan populate job types
    init_db(app)

    # You can also include any additional setup logic, like initializing logs or middleware

    return app


def init_cors(app):
    """Initialize CORS for the application based on the environment."""
    if app.config["ENV"] == "development":
        CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})
    elif app.config["ENV"] == "production":
        CORS(app, resources={r"/*": {"origins": "*"}})
    elif app.config["ENV"] == "staging":
        CORS(app, resources={r"/*": {"origins": ["http://192.168.23.169:8081","http://localhost:5173"]}})

def init_db(app):
    """Inisialisasi database, drop dan buat tabel jika perlu."""
    with app.app_context():
        try:
            # Membuat ulang semua tabel
            db.create_all()  
            print("Tabel user_profile dan tabel lainnya telah dibuat!")

        except Exception as e:
            print(f"Terjadi kesalahan saat inisialisasi database: {e}")