from flask import Blueprint, request, jsonify
from controllers.auth_controller import signup_user, login_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    result, status_code = signup_user(email, password)
    return jsonify(result), status_code

@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    result, status_code = login_user(email, password)
    return jsonify(result), status_code
