from flask import Flask
from config import Config
from models import db
from models.job_type import JobType
from models.user_profile import UserProfile
from controllers.auth_controller import auth_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def init_cors(app):
    """Inisialisasi CORS berdasarkan lingkungan."""
    if app.config["ENV"] == "development":
        cors = CORS(app, resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173",  # Local development
                    "http://192.168.23.169:8081",  # Frontend staging
                ]
            }
        })
    elif app.config["ENV"] == "production":
        cors = CORS(app, resources={
            r"/*": {
                "origins": [
                    "http://192.168.23.169",  # Frontend production
                ]
            }
        })

def init_db(app):
    """Inisialisasi database, drop dan buat tabel jika perlu."""
    with app.app_context():
        try:
            # # Menghapus semua tabel jika ada
            # db.drop_all()  
            # print("Semua tabel telah dihapus!")

            # Membuat ulang semua tabel
            db.create_all()  
            # print("Tabel user_profile dan tabel lainnya telah dibuat!")

        except Exception as e:
            print(f"Terjadi kesalahan saat inisialisasi database: {e}")

def populate_job_types():
    """Mengisi tabel job_type dengan pilihan dropdown hanya jika tabel kosong."""
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
        # Cek apakah ada data dalam job_type
        if not JobType.query.first():  # Cek jika tabel kosong
            for label_en, label_id in job_types:
                value = label_en.replace(" ", "_").lower()  # Membuat nilai yang unik dari label_en
                JobType.create(label_id, label_en, value)
            print("Job types telah ditambahkan ke database!")
        else:
            print("Job types sudah ada di database, tidak perlu ditambahkan.")

# Inisialisasi Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi konfigurasi
Config.init_app(app)

# Inisialisasi JWT
jwt = JWTManager(app)  # Menambahkan JWTManager ke aplikasi

# Inisialisasi database
db.init_app(app)

# Inisialisasi CORS
init_cors(app)

# Daftarkan Blueprint auth
app.register_blueprint(auth_bp, url_prefix='/auth')

# Inisialisasi database dan populate job types
init_db(app)
populate_job_types()

# Menjalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
