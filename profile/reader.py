# profile/reader.py
import csv
import os
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_file_path(filename):
    """Helper function to get absolute file path"""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(current_dir, filename)

def read_cities():
    """Read cities from CSV file and return as a list of dictionaries"""
    try:
        file_path = get_file_path('city_name.csv')
        cities_df = pd.read_csv(file_path)
        return cities_df.to_dict('records')
    except Exception as e:
        logger.error(f"Error reading cities: {str(e)}")
        return [
            {'id': '1', 'name': 'Mumbai'},
            {'id': '2', 'name': 'Delhi'},
            {'id': '3', 'name': 'Bangalore'}
        ]

def save_user_profile(name, city_id):
    """Save user profile to CSV file"""
    try:
        file_path = get_file_path('user_profiles.csv')
        file_exists = os.path.exists(file_path)
        
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['name', 'city_id'])  # Make sure column names match
            writer.writerow([name, city_id])
        logger.debug(f"Saved profile for {name} with city_id {city_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving profile: {str(e)}")
        return False

def get_all_profiles():
    """Get all profiles with city names"""
    try:
        profiles_path = get_file_path('user_profiles.csv')
        cities_path = get_file_path('city_name.csv')

        # Check if files exist and are not empty
        if not os.path.exists(profiles_path):
            logger.warning("No profiles file found")
            return []

        # Log the contents of both files for debugging
        logger.debug(f"Reading profiles from: {profiles_path}")
        logger.debug(f"Reading cities from: {cities_path}")

        # Read the CSVs and log their contents
        profiles_df = pd.read_csv(profiles_path)
        cities_df = pd.read_csv(cities_path)

        logger.debug(f"Profiles DataFrame columns: {profiles_df.columns.tolist()}")
        logger.debug(f"Cities DataFrame columns: {cities_df.columns.tolist()}")
        
        # Ensure the city_id in profiles matches the id in cities
        cities_df = cities_df.rename(columns={'id': 'city_id'})

        # Merge DataFrames
        merged_df = pd.merge(
            profiles_df,
            cities_df,
            on='city_id',
            how='left'
        )

        logger.debug(f"Merged DataFrame columns: {merged_df.columns.tolist()}")

        # Format the result
        result = []
        for _, row in merged_df.iterrows():
            result.append({
                'User Name': row['name_x'],
                'City': row['name_y']
            })

        logger.debug(f"Retrieved {len(result)} profiles: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in get_all_profiles: {str(e)}", exc_info=True)
        return []