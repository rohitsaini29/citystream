from functools import wraps
from flask import request, jsonify, current_app
import secrets

def require_api_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('X-API-Token')
        if not token:
            return jsonify({'error': 'API token is missing'}), 401
        if not secrets.compare_digest(token, current_app.config['API_TOKEN']):
            return jsonify({'error': 'Invalid API token'}), 401
        return f(*args, **kwargs)
    return decorated_function