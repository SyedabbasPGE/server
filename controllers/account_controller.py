from flask import request, jsonify
from models.account import Account

def create_account():
    data = request.json
    required_fields = ["username", "profileImage", "isActive", "posts", "time"]

    # Validate incoming data
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    try:
        account_id = Account.create_account(data)
        return jsonify({"message": "Account created successfully", "id": account_id}), 201
    except Exception as e:
        print("Error creating account:", e)
        return jsonify({"error": "Internal server error"}), 500

def get_all_accounts():
    try:
        accounts = Account.get_all_accounts()
        return jsonify(accounts), 200
    except Exception as e:
        print("Error fetching accounts:", e)
        return jsonify({"error": "Internal server error"}), 500

def delete_account(account_id):
    try:
        result = Account.delete_account(account_id)
        if result.deleted_count > 0:
            return jsonify({"message": "Account deleted successfully"}), 200
        else:
            return jsonify({"error": "Account not found"}), 404
    except Exception as e:
        print("Error deleting account:", e)
        return jsonify({"error": "Internal server error"}), 500
