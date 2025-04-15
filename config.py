import os
from dotenv import load_dotenv

load_dotenv()  # Memuat variabel lingkungan dari file .env

class Config:
    """Konfigurasi dasar untuk aplikasi Flask."""

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')  # Default jika tidak ada

    # Environment Configuration (development, production, etc.)
    ENV = os.getenv('FLASK_ENV', 'development')

    @classmethod
    def get_database_uri(cls):
        """Return the database URI."""
        return cls.SQLALCHEMY_DATABASE_URI

    @classmethod
    def get_flask_env(cls):
        """Return the current environment (development, production)."""
        return cls.ENV

