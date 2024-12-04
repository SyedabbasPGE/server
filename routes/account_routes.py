from flask import Blueprint
from controllers.account_controller import create_account, get_all_accounts, delete_account

account_bp = Blueprint("accounts", __name__)

# Define account routes
account_bp.route("/", methods=["POST"])(create_account)
account_bp.route("/", methods=["GET"])(get_all_accounts)
account_bp.route("/<string:account_id>", methods=["DELETE"])(delete_account)
