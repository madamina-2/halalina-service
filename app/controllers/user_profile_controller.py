from flask import Blueprint, request, jsonify
from models.user_profile import UserProfile
from models.job_type import JobType
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    job_type_value = data.get('job_type')  # Mendapatkan value job type
    married = data.get('married')
    dept_type = data.get('dept_type')
    account_balance = data.get('account_balance')
    age_group = data.get('age_group')

    # Cek apakah job_type_value valid
    job_type = JobType.query.filter_by(value=job_type_value).first()
    if not job_type:
        return jsonify({"message": "Invalid job type"}), 400

    # Membuat profil baru
    new_profile = UserProfile.create(
        user_id=current_user_id,
        job_type_id=job_type.id,  # Menggunakan job_type.id sebagai foreign key
        married=married,
        dept_type=dept_type,
        account_balance=account_balance,
        age_group=age_group
    )

    return jsonify({"message": "User profile created", "profile_id": new_profile.id}), 201

# Mengambil profil pengguna berdasarkan user_id
@user_profile_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()  # Hanya bisa diakses oleh pengguna yang sudah login
def get_profile(user_id):
    current_user_id = get_jwt_identity()

    # Periksa apakah pengguna yang diminta sesuai dengan pengguna yang login
    if current_user_id != user_id:
        return jsonify({"message": "You are not authorized to view this profile"}), 403

    # Mengambil profil berdasarkan user_id
    profile = UserProfile.get_profile_by_user_id(user_id)

    if profile:
        return jsonify({
            "user_id": profile.user_id,
            "job_type": profile.job_type.label_en,  # Menampilkan label job type
            "married": profile.married,
            "dept_type": profile.dept_type,
            "account_balance": profile.account_balance,
            "age_group": profile.age_group
        }), 200
    else:
        return jsonify({"message": "Profile not found"}), 404
