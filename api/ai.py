from flask import Blueprint, jsonify, request
import json
import os
from flask_cors import CORS, cross_origin
from model.reco import add_book_to_db, db

ai_api = Blueprint('ai_api', __name__, url_prefix='/api')
CORS(ai_api)  # to allow the frontend to access the API

@ai_api.route('/', methods=['GET'])  # test if the server is running correctly
@cross_origin()
def home():
    return "Welcome to the Book Adaptations API!"

def load_books():  # function to load the books from the json file (books.json)
    try:
        with open('books.json') as f:
            return json.load(f), None
    except FileNotFoundError:  # if the file is not found return an error message
        return {}, "File not found."
    except json.JSONDecodeError:
        return {}, "Error decoding JSON."

def save_books(books):  # function to save the books to the json file (books.json)
    try:
        with open('books.json', 'w') as f:
            json.dump(books, f)
        return None
    except Exception as e:
        return str(e)

@ai_api.route('/recommendations', methods=['GET'])  # get all the books
@cross_origin()
def get_books():
    books, error = load_books()
    if error:
        return jsonify({"error": error}), 500

    genre = request.args.get('genre', None)
    
    # Filter books based on the genre
    if genre and genre in books:
        recommended_books = books[genre]
    else:
        recommended_books = [book for genre_books in books.values() for book in genre_books]
    
    return jsonify(recommended_books)

@ai_api.route('/books', methods=['POST'])  # add a new book
@cross_origin()
def add_book():
    new_book = request.json
    try:
        added_book = add_book_to_db(new_book)
        return jsonify({
            'id': added_book.id,
            'title': added_book.title,
            'author': added_book.author,
            'genre': added_book.genre
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(ai_api)
    app.run(debug=True, port=5000)
