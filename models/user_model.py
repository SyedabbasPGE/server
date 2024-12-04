import uuid

def get_uuid():
    return str(uuid.uuid4())

def create_user(email, hashed_password, db):
    user_id = get_uuid()
    new_user = {"id": user_id, "email": email, "password": hashed_password}
    db.users.insert_one(new_user)
    return user_id

def get_user_by_email(email, db):
    return db.users.find_one({"email": email})

def get_user_by_id(user_id, db):
    return db.users.find_one({"id": user_id})

def get_user_accounts(user_id, db):
    return list(db.accounts.find({"user_id": user_id}))  # Modify as per your database structure
