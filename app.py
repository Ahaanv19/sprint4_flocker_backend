from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/books', methods=['GET'])
def get_books():
    books = [
        {"title": "1984", "author": "George Orwell", "genre": "Dystopian"},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction"},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic"}
    ]
    return jsonify(books)

if __name__ == "__main__":
    app.run(port=3000)

