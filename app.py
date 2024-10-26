# app.py
from flask import Flask
from profile.routes import profile_bp
import os
import secrets

app = Flask(__name__)

# Generate a secure API token
API_TOKEN = os.environ.get('API_TOKEN') or secrets.token_urlsafe(32)
app.config['API_TOKEN'] = API_TOKEN
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY') or secrets.token_hex(16)

# Register the blueprint
app.register_blueprint(profile_bp)

if __name__ == '__main__':
    if not os.environ.get('API_TOKEN'):
        print(f"\nAPI Token (save this securely): {API_TOKEN}")
    if not os.environ.get('FLASK_SECRET_KEY'):
        print(f"Secret Key: {app.config['SECRET_KEY']}")
    app.run(host='0.0.0.0', port=3000, debug=True)