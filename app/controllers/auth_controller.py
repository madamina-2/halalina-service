from flask import Blueprint, request, jsonify
from models.user import User
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

# Blueprint untuk autentikasi
auth_bp = Blueprint('auth', __name__)

# Rute untuk Register User
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email').lower() if data.get('email') else None
    password = data.get('password')
    phone_number = data.get('phone_number')

    # Validasi input
    if not full_name or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # Validasi format email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return jsonify({"message": "Invalid email format"}), 400

    # Validasi password: minimal 1 huruf besar, 1 huruf kecil, 1 angka, dan 1 simbol
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if not re.match(password_regex, password):
        return jsonify({
            "message": "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
        }), 400

    # Validasi nomor telepon
    phone_regex = r'^\+?\d+$'  # Hanya angka dan simbol '+' yang diperbolehkan
    if not re.match(phone_regex, phone_number):
        return jsonify({"message": "Phone number can only contain numbers and '+' symbol"}), 400

    # Mengganti +62 atau 62 dengan 0 pada nomor telepon
    phone_number = phone_number.replace('+62', '0').replace('62', '0')

    # Cek apakah email atau nomor telepon sudah terdaftar
    if User.get_user_by_email(email):
        return jsonify({"message": "Email already exists"}), 400
    if User.get_user_by_phone_number(phone_number):
        return jsonify({"message": "Phone number already exists"}), 400

    # Hash password sebelum menyimpan
    hashed_password = generate_password_hash(password)

    # Buat user baru
    new_user = User.create(full_name, email, hashed_password, phone_number)

    # Buat JWT tokens (access token dan refresh token)
    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)

    return jsonify({
        "message": f"User {new_user.full_name} registered successfully!",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 201

# Rute untuk Login User
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validasi input
    if not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # Cek apakah user ada
    user = User.get_user_by_email(email)
    if not user:
        return jsonify({"message": "Invalid email or password"}), 400

    # Verifikasi password
    if not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 400

    # Buat JWT tokens (access token dan refresh token)
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


# Rute untuk mendapatkan Access Token baru menggunakan Refresh Token
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Pastikan hanya refresh token yang valid yang bisa mengakses endpoint ini
def refresh():
    # Mendapatkan user_id dari refresh token
    current_user_id = get_jwt_identity()

    # Membuat access token baru
    access_token = create_access_token(identity=current_user_id)

    return jsonify({
        "access_token": access_token  # Kembalikan access token baru
    }), 200
