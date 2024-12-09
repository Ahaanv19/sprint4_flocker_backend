from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory database (list of books)
books = [
    {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"title": "1984", "author": "George Orwell"}
]

# API endpoint to fetch all books
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(books)

# API endpoint to add a new book
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = {"title": data["title"], "author": data["author"]}
    books.append(new_book)
    return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(port=3000)




