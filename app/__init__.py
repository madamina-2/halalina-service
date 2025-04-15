from flask import Flask
from app.models.job_type import JobType
from config import Config
from app.models import db
from app.controllers import auth_bp, user_profile_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager


def create_app():
    """Factory function to create and configure the Flask app."""
    
    # Create a Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)

    # Initialize database (SQLAlchemy)
    db.init_app(app)
    
    # Initialize JWT manager for handling tokens
    JWTManager(app)
    
    # Set up CORS based on environment configuration
    init_cors(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register auth routes
    app.register_blueprint(user_profile_bp, url_prefix='/user_profile')  # Register user profile routes

    # Inisialisasi database dan populate job types
    init_db(app)
    populate_job_types(app)

    # You can also include any additional setup logic, like initializing logs or middleware

    return app


def init_cors(app):
    """Initialize CORS for the application based on the environment."""
    if app.config["ENV"] == "development":
        CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://192.168.23.169:8081"]}})
    elif app.config["ENV"] == "production":
        CORS(app, resources={r"/*": {"origins": ["http://192.168.23.169"]}})

def init_db(app):
    """Inisialisasi database, drop dan buat tabel jika perlu."""
    with app.app_context():
        try:
            # Menghapus semua tabel jika ada
            db.drop_all()  
            print("Semua tabel telah dihapus!")

            # Membuat ulang semua tabel
            db.create_all()  
            print("Tabel user_profile dan tabel lainnya telah dibuat!")

        except Exception as e:
            print(f"Terjadi kesalahan saat inisialisasi database: {e}")

def populate_job_types(app):
    """Mengisi tabel job_type dengan pilihan dropdown."""
    job_types = [
        ('domestic worker', 'Pekerja Rumah Tangga'),
        ('construction worker', 'Pekerja Konstruksi'),
        ('factory worker', 'Pekerja Pabrik'),
        ('technician', 'Teknisi'),
        ('driver', 'Pengemudi'),
        ('security personnel', 'Personel Keamanan'),
        ('maintenance worker', 'Pekerja Pemeliharaan'),
        ('farmer', 'Petani'),
        ('manager', 'Manajer'),
        ('engineer', 'Insinyur'),
        ('accountant', 'Akuntan'),
        ('doctor', 'Dokter'),
        ('lawyer', 'Pengacara'),
        ('office staff', 'Staf Kantor'),
        ('analyst', 'Analis'),
        ('business owner', 'Pemilik Bisnis'),
        ('freelancer', 'Pekerja Lepas'),
        ('self-employed', 'Wiraswasta'),
        ('consultant', 'Konsultan'),
        ('retired', 'Pensiunan'),
        ('student', 'Mahasiswa')
    ]

    with app.app_context():
        for label_en, label_id in job_types:
            value = label_en.replace(" ", "_").lower()  # Membuat nilai yang unik dari label_en
            JobType.create(label_id, label_en, value)