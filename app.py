from flask import Flask
from profile.routes import profile_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Register the blueprint
app.register_blueprint(profile_bp)

if __name__ == '__main__':
    # You can specify both host and port
    app.run(host='0.0.0.0', port=3000, debug=True)
    # Or just the port
    # app.run(port=8080, debug=True)