from flask import Flask, Blueprint, jsonify, request
from flask_cors import cross_origin, CORS
import json
import os

# Initialize Blueprint and CORS
recomendations_api = Blueprint('recomendations_api', __name__)
CORS(recomendations_api)

# Load books from the Books.json file (relative path)
book_file_path = os.path.join(os.path.dirname(__file__), '../Books.json')
def load_recomendations():
    try:
        with open(book_file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}, "File not found."
    except json.JSONDecodeError:
        return {}, "Error decoding JSON."

# Home route to test if the server is running
@recomendations_api.route('/', methods=['GET'])
@cross_origin()
def home():
    return "Welcome to the Book Recommendations API!"

# Endpoint to get book recommendations based on genre or all books
@recomendations_api.route('/recommendations', methods=['GET'])
@cross_origin()
def get_recomendations():
    recomendations, error = load_recomendations()
    if error:
        return jsonify({"error": error}), 500

    genre = request.args.get('genre', None)
    
    # Filter books based on the genre
    if genre and genre in recomendations:
        recommended_books = recomendations[genre]
    else:
        recommended_books = [book for genre_books in recomendations.values() for book in genre_books]
    
    return jsonify(recommended_books)
    
   
# Running on port 8887
if __name__ == '__main__':
    # Set logging level to debug to show logs in the terminal
    recomendations_api.run(debug=True, port=8887)
