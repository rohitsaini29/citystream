CityStream

CityStream is a Flask web application that allows users to submit their profiles, including their name and city, which are then stored in a CSV file. The app also features an admin panel for viewing submitted profiles and a token-based API for secure interactions.

Features
User Profile Submission: Users can submit their name and city via a web form.
Admin Panel: Admin users can log in to view all submitted profiles.
Error Handling: Comprehensive error handling ensures smooth user experience:
Checks for empty fields in form submissions.
Invalid login credentials are handled with appropriate error messages.
Logging of important events and errors for debugging.
CSV Storage: User profiles are stored in a CSV file, allowing for easy data management.
Token-Based API: Enhanced security for API interactions.
Technologies Used
Flask: A lightweight WSGI web application framework.
Bootstrap: For responsive web design.
Pandas: For data manipulation and CSV file handling.
Logging: For tracking application events and errors.