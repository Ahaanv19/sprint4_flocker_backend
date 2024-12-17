from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Load environment variables from .env file
load_dotenv(dotenv_path='/Users/jacobzierolf/nighthawk/sprint4_flocker_backend/password.env')

# Configure CORS to allow requests from your frontend
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:4887", "supports_credentials": True}})

# Initialize HTTP Basic Authentication
auth = HTTPBasicAuth()

# Define users and passwords
users = {
    os.getenv('ADMIN_USER'): os.getenv('ADMIN_PASSWORD'),
    os.getenv('DEFAULT_USER'): os.getenv('DEFAULT_PASSWORD')
}

# Verify password
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None

# Handle preflight requests
@app.before_request
def handle_options_requests():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = response.headers

        headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:4887'
        headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, x-api-key, Accept, Origin, X-Requested-With'
        headers['Access-Control-Allow-Credentials'] = 'true'

        return response

# Define a route for the root URL
@app.route('/')
def home():
    return 'Hello, World!'

# Define a login route with Basic Authentication
@app.route('/login', methods=['GET'])
@auth.login_required
def login():
    return jsonify({'message': 'Login successful', 'user': auth.current_user()})

# Define a logout route
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout successful'})

# User information endpoint
@app.route('/api/user', methods=['GET'])
def get_user_info():
    user_info = {
        "name": "Ahaan Vaidyanathan",
        "age": 15,
        "city": "San Diego",
        "hobbies": ["Video Games", "Coding", "Modeling"]
    }
    return jsonify(user_info)

# Pre-populated book list
books = [
    {"title": "The Hunger Games", "author": "Suzanne Collins"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"title": "1984", "author": "George Orwell"}
]

# Get all books
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Add a new book
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = {"title": data['title'], "author": data['author']}
    books.append(new_book)
    return jsonify({"message": "Book added successfully!"}), 201

# Define a route to get user ID
@app.route('/api/id', methods=['GET'])
@auth.login_required
def get_id():
    user_id = {"id": 123}  # Example static ID, replace with actual logic if needed
    return jsonify(user_id)

# Define a route to get static data
@app.route('/api/staticData', methods=['GET'])
@auth.login_required
def get_data():
    staticData = ["data point 1", "data point 2", "data point 3"]
    return jsonify(staticData)

if __name__ == '__main__':
    app.run(port=8887, debug=True)

