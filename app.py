from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv(dotenv_path='/Users/jacobzierolf/nighthawk/sprint4_flocker_backend/password.env')

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
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

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

staticData = ["data point 1", "data point 2", "data point 3"]

@app.route('/api/staticData', methods=['GET'])
def get_data():
    return jsonify(staticData)

if __name__ == '__main__':
    app.run(port=8887, debug=True)

