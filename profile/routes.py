from flask import Blueprint, render_template, request, redirect, url_for, flash
from .reader import read_cities, save_user_profile

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET', 'POST'])
def profile_form():
    if request.method == 'POST':
        name = request.form.get('name')
        city_id = request.form.get('city')
        
        # Basic form validation
        if not name or not city_id:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('profile.profile_form'))
        
        # Save the user profile
        save_user_profile(name, city_id)
        flash('Profile saved successfully!', 'success')
        return redirect(url_for('profile.profile_form'))
    
    # Get cities for the dropdown
    cities = read_cities()
    return render_template('form.html', cities=cities)