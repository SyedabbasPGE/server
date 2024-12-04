import os
from flask import Flask
from routes.auth_routes import auth_bp
from routes.account_routes import account_bp
from routes.schedulepost_routes import schedulepost_bp
from flask_cors import CORS
from config import load_environment_variables

# Load environment variables
load_environment_variables()

# Initialize the Flask app
app = Flask(__name__)

# Set secret key from environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

# Enable CORS for specific origin (Frontend URL)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}}, supports_credentials=True)


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(account_bp, url_prefix="/api/accounts")
app.register_blueprint(schedulepost_bp, url_prefix="/api/schedulepost")

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
