from flask import Flask, jsonify, request, session
from flask_cors import CORS
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Load environment variables from .env file
load_dotenv(dotenv_path='/Users/jacobzierolf/nighthawk/sprint4_flocker_backend/password.env')

# Configure CORS to allow requests from your frontend
CORS(app, resources={r'*': {"origins": os.getenv('CORS_ORIGINS', 'http://127.0.0.1:5000'), "supports_credentials": True}})

# Handle preflight requests
@app.before_request
def handle_options_requests():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = response.headers

        headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5000'
        headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        headers['Access-Control-Allow-Credentials'] = 'true'

        return response

# Define a route for the root URL
@app.route('/')
def home():
    return 'Hello, World!'

# Define a login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    admin_user = os.getenv('ADMIN_USER')
    admin_password = os.getenv('ADMIN_PASSWORD')
    default_user = os.getenv('DEFAULT_USER')
    default_password = os.getenv('DEFAULT_PASSWORD')

    if (username == admin_user and password == admin_password) or (username == default_user and password == default_password):
        session['username'] = username
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Define a logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
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
def get_id():
    if 'username' in session:
        user_id = {"id": 123}  # Example static ID, replace with actual logic if needed
        return jsonify(user_id)
    else:
        return jsonify({'message': 'Unauthorized'}), 401

# Define a route to get static data
@app.route('/api/staticData', methods=['GET'])
def get_data():
    staticData = ["data point 1", "data point 2", "data point 3"]
    return jsonify(staticData)

if __name__ == '__main__':
    app.run(port=8887, debug=True)

