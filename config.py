import os
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import urlparse
import cloudinary

# Load environment variables
def load_environment_variables():
    load_dotenv()

# Load environment variables
load_environment_variables()

# Get MongoDB URI and JWT secret key from environment variables
mongo_uri = os.getenv("MONGO_URI")
jwt_secret_key = os.getenv("JWT_SECRET_KEY")

if not mongo_uri:
    raise ValueError("MONGO_URI is not defined in the .env file.")

if not jwt_secret_key:
    raise ValueError("JWT_SECRET_KEY is not defined in the .env file.")

client = MongoClient(mongo_uri)

# Explicitly extract the database name from the URI or fallback to 'db1'
db_name = urlparse(mongo_uri).path.lstrip('/') or "db1"
db = client[db_name]

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)
