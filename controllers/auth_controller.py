import datetime
import jwt
import uuid
from flask_bcrypt import generate_password_hash, check_password_hash
from config import db, jwt_secret_key

# Helper function to create a JWT
def create_jwt(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode(
        {"user_id": user_id, "exp": expiration_time},
        jwt_secret_key,
        algorithm="HS256"
    )
    return token.decode('utf-8') if isinstance(token, bytes) else token

def signup_user(email, password):
    existing_user = db.users.find_one({"email": email})
    if existing_user:
        return {"error": "Email already exists"}, 409

    hashed_password = generate_password_hash(password).decode('utf-8')
    user_id = str(uuid.uuid4())
    new_user = {"id": user_id, "email": email, "password": hashed_password}
    db.users.insert_one(new_user)

    return {"id": user_id, "email": email}, 201

def login_user(email, password):
    user = db.users.find_one({"email": email})
    if not user or not check_password_hash(user['password'], password):
        return {"error": "Unauthorized Access"}, 401

    token = create_jwt(user["id"])
    return {"token": token, "email": user["email"]}, 200
