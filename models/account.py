from config import db
from bson import ObjectId

# MongoDB collection for accounts
accounts_collection = db.accounts

class Account:
    @staticmethod
    def create_account(account_data):
        """Inserts a new account into the database."""
        result = accounts_collection.insert_one(account_data)
        return str(result.inserted_id)  # Return the ID of the newly created account

    @staticmethod
    def get_all_accounts():
        """Fetches all accounts from the database."""
        accounts = list(accounts_collection.find({}))
        # Transform _id to id
        for account in accounts:
            account["id"] = str(account["_id"])
            del account["_id"]
        return accounts

    @staticmethod
    def update_account(username, update_data):
        """Updates an account's details."""
        return accounts_collection.update_one({"username": username}, {"$set": update_data})

    @staticmethod
    def delete_account(account_id):
        """Deletes an account by its ID."""
        return accounts_collection.delete_one({"_id": ObjectId(account_id)})
