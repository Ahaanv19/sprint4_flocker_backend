from flask import Blueprint, jsonify, request
import json
import os
from flask_cors import CORS, cross_origin

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

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(ai_api)
    app.run(debug=True, port=8887)
