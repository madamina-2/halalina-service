from flask import jsonify

def make_response(response_code, message, data=None):
    """Fungsi untuk mengembalikan response dengan format tertentu"""
    response = {
        "responseCode": response_code,
        "message": message,
        "data": data if data else {}
    }
    return jsonify(response), response_code
