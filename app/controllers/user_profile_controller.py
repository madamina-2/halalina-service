import os
import requests
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user_profile import UserProfile
from app.models.user import User
from app.models.job_type import JobType
from app.utils import make_response
from dotenv import load_dotenv

load_dotenv()

user_profile_bp = Blueprint('user_profile', __name__)

# Validasi input untuk marital status
def validate_marital_status(married):
    if married not in ['single', 'married']:
        raise ValueError("Status perkawinan tidak ditemukan. harus 'single' atau 'married'")

# Validasi input untuk age group
def validate_age_group(age_group):
    if age_group not in ['gen_Z', 'millennials', 'gen_X']:
        raise ValueError("Kelompok usia tidak ditemukan. Harus 'gen_Z', 'millennials', atau 'gen_X'")

# Membaca pemetaan job type dari environment variable
blue_collar_jobs = os.getenv("BLUE_COLLAR", "").split(",")
white_collar_jobs = os.getenv("WHITE_COLLAR", "").split(",")
entrepreneur_jobs = os.getenv("ENTREPRENEUR", "").split(",")
others_jobs = os.getenv("OTHERS", "").split(",")

# Membuat profil pengguna baru
@user_profile_bp.route('/create', methods=['POST'])
@jwt_required()
def create_profile():
    current_user_id = get_jwt_identity()

    data = request.get_json()

    # Validasi input
    try:
        job_type_id = data.get('job_type_id')
        if not job_type_id:
            return make_response(400, "ID job type tidak boleh kosong")

        job_type = JobType.query.filter_by(id=job_type_id).first()
        if not job_type:
            return make_response(400, "ID job type tidak ditemukan")

        married = data.get('married')
        validate_marital_status(married)

        debt_type = data.get('debt_type')
        if not isinstance(debt_type, list):
            return make_response(400, "Debt type harus dalam bentuk array")

        account_balance = data.get('account_balance')
        if not isinstance(account_balance, int) or account_balance < 0:
            return make_response(400, "Saldo tidak boleh negatif")

        age_group = data.get('age_group')
        validate_age_group(age_group)

        # Membuat profil baru
        new_profile = UserProfile.create(
            user_id=current_user_id,
            job_type_id=job_type.id,
            married=married,
            debt_type=debt_type,
            account_balance=account_balance,
            age_group=age_group
        )

        return make_response(201, "Berhasil menyimpan data", {"profile_id": new_profile.id})

    except ValueError as e:
        return make_response(422, str(e))

# Mengambil profil pengguna berdasarkan user_id
@user_profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()

    # Mengambil profil berdasarkan user_id
    profile = UserProfile.get_profile_by_user_id(current_user_id)
    user = User.get_user_by_id(current_user_id)

    if profile:
        return make_response(200, "Profil ditemukan", {
            "user_id": profile.user_id,
            "user_name": user.full_name,
            "job_type": profile.job_type.label_en,
            "married": profile.married,
            "debt_type": profile.debt_type,
            "account_balance": profile.account_balance,
            "age_group": profile.age_group
        })
    else:
        return make_response(404, "Profil tidak ditemukan")
    
# Route to get all job types
@user_profile_bp.route('/job_type', methods=['GET'])
@jwt_required()
def get_job_type():
    # Mengambil seluruh data job type
    job_types = JobType.get_all_job_types()

    if job_types:
        # Mengembalikan daftar job type
        job_type_list = [{"id": job.id, "label_id": job.label_id, "label_en": job.label_en, "value": job.value} for job in job_types]
        
        return make_response(200, "Sukses mengambil data", {"job_types": job_type_list})
    else:
        return make_response(404, "Job types tidak ditemukan")


# New endpoint to get prediction from halalina-ml
@user_profile_bp.route('/predict', methods=['POST'])
@jwt_required()
def get_prediction_from_halalina_service():
    # Mendapatkan header Authorization dan mengambil token JWT secara penuh
    auth_header = request.headers.get('Authorization', None)
    token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
    current_user_id = get_jwt_identity()
    # Mengambil profil berdasarkan user_id
    profile = UserProfile.get_profile_by_user_id(current_user_id)
    
    if not profile:
        return make_response(404, "Isi data profil dulu")
        

    # Logic untuk memetakan job_type ke kategori
    job_type = profile.job_type.label_en  # Retrieve job_type from profile
    if job_type in blue_collar_jobs:
        job_type_parent = 'blue-collar'
    elif job_type in white_collar_jobs:
        job_type_parent = 'white-collar'
    elif job_type in entrepreneur_jobs:
        job_type_parent = 'entrepreneur'
    elif job_type in others_jobs:
        job_type_parent = 'others'
    else:
        job_type_parent = 'others'  # Default to 'others' if not in any category

    # Data untuk dikirim ke halalina-ml
    data = {
        'job': job_type_parent,
        'marital': profile.married,
        'balance': profile.account_balance,
        'age_group': profile.age_group.lower(),
        'is_having_debt': len(profile.debt_type)  # Jumlah debt_type sebagai indikator
    }

    halalina_ml_url = os.getenv("HALALINA_ML_URL", "http://127.0.0.1:5000/api/predict")

    # Kirim request ke halalina-ml untuk mendapatkan prediksi
    try:
        response = requests.post(
            halalina_ml_url,  # Ganti dengan alamat endpoint yang sesuai
            json=data,
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Jika request berhasil
        if response.status_code == 200:
            prediction_data = response.json()
            return make_response(200, "Prediksi berhasil didapatkan", prediction_data)
        else:
            return make_response(response.status_code, response.text)

    except Exception as e:
        return make_response(500, f"Gagal berkomunikasi dengan halalina-ml: {str(e)}")
