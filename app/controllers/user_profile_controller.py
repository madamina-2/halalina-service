from flask import Blueprint, request, jsonify
from models.user_profile import UserProfile
from models.job_type import JobType
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import make_response

# Blueprint untuk UserProfile
user_profile_bp = Blueprint('user_profile', __name__)

# Membuat profil pengguna baru
@user_profile_bp.route('/create', methods=['POST'])
@jwt_required()  # Hanya bisa diakses oleh pengguna yang sudah login
def create_profile():
    # Mengambil user_id dari JWT token
    current_user_id = get_jwt_identity()

    # Mengambil data dari request JSON
    data = request.get_json()
    print("Request Data:", data)

    # Validasi input
    job_type_id = data.get('job_type_id')
    if not job_type_id:
        return make_response(422, "Job type ID is required")
    job_type = JobType.query.filter_by(id=job_type_id).first()
    if not job_type:
        return make_response(422, "Invalid job type ID")

    married = data.get('married')
    if married not in ['single', 'married']:
        return make_response(422, "Invalid marital status. Must be 'single' or 'married'")

    debt_type = data.get('debt_type')
    if not isinstance(debt_type, list):
        return make_response(422, "Debt type must be an array")

    account_balance = data.get('account_balance')
    if not isinstance(account_balance, int) or account_balance < 0:
        return make_response(422, "Account balance must be a non-negative integer")

    age_group = data.get('age_group')
    if age_group not in ['gen_Z', 'millennials', 'gen_X']:
        return make_response(422, "Invalid age group. Must be 'gen_Z', 'millennials', or 'gen_X'")

    # Membuat profil baru
    new_profile = UserProfile.create(
        user_id=current_user_id,
        job_type_id=job_type.id,  # Menggunakan job_type.id sebagai foreign key
        married=married,
        debt_type=debt_type,
        account_balance=account_balance,
        age_group=age_group
    )

    return make_response(201, "User profile created", {"profile_id": new_profile.id})


# Mengambil profil pengguna berdasarkan user_id
@user_profile_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()  # Hanya bisa diakses oleh pengguna yang sudah login
def get_profile(user_id):
    current_user_id = get_jwt_identity()

    # Periksa apakah pengguna yang diminta sesuai dengan pengguna yang login
    if current_user_id != user_id:
        return make_response(403, "You are not authorized to view this profile")

    # Mengambil profil berdasarkan user_id
    profile = UserProfile.get_profile_by_user_id(user_id)

    if profile:
        return jsonify({
            "user_id": profile.user_id,
            "job_type": profile.job_type.label_en,  # Menampilkan label job type
            "married": profile.married,
            "debt_type": profile.debt_type,
            "account_balance": profile.account_balance,
            "age_group": profile.age_group
        }), 200
    else:
        return make_response(404, "Profile not found")
