from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session, jsonify
from .reader import read_cities, save_user_profile, get_all_profiles
from .auth import require_api_token
import logging

logger = logging.getLogger(__name__)

profile_bp = Blueprint('profile', __name__)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# API endpoint to get cities
@profile_bp.route('/api/cities', methods=['GET'])
@require_api_token
def get_cities_api():
    cities = read_cities()
    return jsonify({'cities': cities})

# API endpoint to submit profile
@profile_bp.route('/api/profile', methods=['POST'])
@require_api_token
def submit_profile_api():
    data = request.get_json()
    
    if not data or 'name' not in data or 'city_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if save_user_profile(data['name'], data['city_id']):
        return jsonify({'message': 'Profile saved successfully'}), 201
    else:
        return jsonify({'error': 'Failed to save profile'}), 500

# API endpoint to get all profiles (admin only)
@profile_bp.route('/api/profiles', methods=['GET'])
@require_api_token
def get_profiles_api():
    # Additional admin token check for sensitive data
    admin_token = request.headers.get('X-Admin-Token')
    if not admin_token or admin_token != current_app.config.get('ADMIN_TOKEN', 'admin-secret-token'):
        return jsonify({'error': 'Admin access required'}), 403
    
    profiles = get_all_profiles()
    return jsonify({'profiles': profiles})

# Existing web routes
@profile_bp.route('/', methods=['GET', 'POST'])
def profile_form():
    if request.method == 'POST':
        if 'admin_login' in request.form:
            username = request.form.get('username')
            password = request.form.get('password')

            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['is_admin'] = True
                flash('Admin login successful!', 'success')
            else:
                flash('Invalid credentials!', 'error')
            return redirect(url_for('profile.profile_form'))

        name = request.form.get('name')
        city_id = request.form.get('city')

        if not name or not city_id:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('profile.profile_form'))

        if save_user_profile(name, city_id):
            flash('Profile saved successfully!', 'success')
        else:
            flash('Error saving profile. Please try again.', 'error')
        return redirect(url_for('profile.profile_form'))

    # GET request handling
    cities = read_cities()
    is_admin = session.get('is_admin', False)
    profiles = []
    
    if is_admin:
        profiles = get_all_profiles()
        
    return render_template('form.html', 
                         cities=cities, 
                         is_admin=is_admin, 
                         profiles=profiles,
                         api_token=current_app.config.get('API_TOKEN', ''))

@profile_bp.route('/logout')
def logout():
    session.pop('is_admin', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('profile.profile_form'))