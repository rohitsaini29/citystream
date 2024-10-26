# profile/reader.py
import csv
import os

def read_cities():
    """Read cities from CSV file and return as a list of dictionaries"""
    # Get the absolute path to the city_name.csv file
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, 'city_name.csv')
    
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            cities = []
            for row in csv_reader:
                cities.append({'id': row['id'], 'name': row['name']})
        return cities
    except:
        # If anything goes wrong, return dummy data to keep app running
        return [
            {'id': '1', 'name': 'Mumbai'},
            {'id': '2', 'name': 'Delhi'},
            {'id': '3', 'name': 'Bangalore'}
        ]

def save_user_profile(name, city_id):
    """Save user profile to CSV file"""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, 'user_profiles.csv')
    
    file_exists = os.path.exists(file_path)
    
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['name', 'city_id'])
        writer.writerow([name, city_id])