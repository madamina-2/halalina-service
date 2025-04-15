import os
from dotenv import load_dotenv

load_dotenv()  # Memuat variabel lingkungan dari file .env

class Config:
    """Konfigurasi dasar untuk aplikasi Flask."""

    # Flask secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')  # Default jika tidak ada

    # Environment Configuration (development, production, etc.)
    ENV = os.getenv('FLASK_ENV', 'development')

    # Database Configuration (Dinamis berdasarkan FLASK_ENV)
    @classmethod
    def get_database_uri(cls):
        """Mengembalikan URI database sesuai dengan lingkungan yang digunakan"""
        # Konfigurasi database untuk development, staging, dan production
        if cls.ENV == 'development':
            return f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        
        elif cls.ENV == 'production':
            return f"postgresql://{os.getenv('DB_USERNAME_PROD')}:{os.getenv('DB_PASSWORD_PROD')}@{os.getenv('DB_HOST_PROD')}:{os.getenv('DB_PORT_PROD')}/{os.getenv('DB_NAME_PROD')}"
        
        elif cls.ENV == 'staging':
            return f"postgresql://{os.getenv('DB_USERNAME_STAGING')}:{os.getenv('DB_PASSWORD_STAGING')}@{os.getenv('DB_HOST_STAGING')}:{os.getenv('DB_PORT_STAGING')}/{os.getenv('DB_NAME_STAGING')}"
        
        else:
            raise ValueError("Invalid FLASK_ENV value. Use 'development', 'production', or 'staging'.")

    # SQLALCHEMY_DATABASE_URI akan di-set melalui method class
    SQLALCHEMY_DATABASE_URI = None  # Tidak langsung dipanggil pada saat deklarasi kelas
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # Default 1 jam
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 86400))  # Default 1 hari

    @classmethod
    def init_app(cls, app):
        """Inisialisasi aplikasi dengan konfigurasi ini"""
        app.config.from_object(cls)

        # Setel SQLALCHEMY_DATABASE_URI setelah kelas diinisialisasi
        cls.SQLALCHEMY_DATABASE_URI = cls.get_database_uri()
        app.config['SQLALCHEMY_DATABASE_URI'] = cls.SQLALCHEMY_DATABASE_URI
