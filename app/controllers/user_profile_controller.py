import os
import requests
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user_profile import UserProfile
from app.models.job_type import JobType
from app.utils import make_response
from dotenv import load_dotenv

load_dotenv()

user_profile_bp = Blueprint('user_profile', __name__)

# Validasi input untuk marital status
def validate_marital_status(married):
    if married not in ['single', 'married']:
        raise ValueError("Invalid marital status. Must be 'single' or 'married'")

# Validasi input untuk age group
def validate_age_group(age_group):
    if age_group not in ['gen_Z', 'millennials', 'gen_X']:
        raise ValueError("Invalid age group. Must be 'gen_Z', 'millennials', or 'gen_X'")

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
            return make_response(400, "Job type ID is required")

        job_type = JobType.query.filter_by(id=job_type_id).first()
        if not job_type:
            return make_response(400, "Invalid job type ID")

        married = data.get('married')
        validate_marital_status(married)

        debt_type = data.get('debt_type')
        if not isinstance(debt_type, list):
            return make_response(400, "Debt type must be an array")

        account_balance = data.get('account_balance')
        if not isinstance(account_balance, int) or account_balance < 0:
            return make_response(400, "Account balance must be a non-negative integer")

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

        return make_response(201, "User profile created", {"profile_id": new_profile.id})

    except ValueError as e:
        return make_response(422, str(e))

# Mengambil profil pengguna berdasarkan user_id
@user_profile_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_profile(user_id):
    current_user_id = get_jwt_identity()

    # Periksa apakah pengguna yang diminta sesuai dengan pengguna yang login
    if current_user_id != user_id:
        return make_response(403, "You are not authorized to view this profile")

    # Mengambil profil berdasarkan user_id
    profile = UserProfile.get_profile_by_user_id(user_id)

    if profile:
        return make_response(200, "Profile found", {
            "user_id": profile.user_id,
            "job_type": profile.job_type.label_en,
            "married": profile.married,
            "debt_type": profile.debt_type,
            "account_balance": profile.account_balance,
            "age_group": profile.age_group
        })
    else:
        return make_response(404, "Profile not found")


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

    halalina_ml_url = os.getenv("HALALINA_ML_URL", "http://127.0.0.1:5000/predict")

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
            return make_response(200, "Prediction received successfully", prediction_data)
        else:
            return make_response(response.status_code, response.text)

    except Exception as e:
        return make_response(500, f"Error while communicating with halalina-ml: {str(e)}")
