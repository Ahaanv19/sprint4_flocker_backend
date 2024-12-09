from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run(port=3000)

