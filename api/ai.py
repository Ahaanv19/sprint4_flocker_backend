from flask import Flask, Blueprint, jsonify, request
import random
from flask_cors import cross_origin
import json
import os
from flask import Blueprint, jsonify, request
from flask_cors import CORS


ai_api = Blueprint('ai_api', __name__)
CORS(ai_api)
# Predefined list of books
books = [
    {"title": "The Hunger Games", "author": "Suzanne Collins", "genre": "Dystopian"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic"},
    {"title": "1984", "author": "George Orwell", "genre": "Dystopian"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic"},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "genre": "Fantasy"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy"},
    {"title": "Moby Dick", "author": "Herman Melville", "genre": "Adventure"},
    {"title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Classic"}
]

# Endpoint to get book recommendations
@ai_api.route('/recommendations', methods=['GET'])
@cross_origin()  # Allow cross-origin requests
def recommendations():
    genre = request.args.get('genre', None)  # Get genre from query parameter

    # Debug logging to see the received genre
    ai_api.logger.debug(f"Received genre: {genre}")

    # If genre is provided, filter books by genre
    if genre:
        recommended_books = [book for book in books if book['genre'].lower() == genre.lower()]
        ai_api.logger.debug(f"Filtered books by genre '{genre}': {recommended_books}")
    else:
        # If no genre is provided, return all books
        recommended_books = books
        ai_api.logger.debug("No genre filter applied, returning all books.")

    # Randomly select up to 3 books from the filtered list
    recommendations = random.sample(recommended_books, min(3, len(recommended_books)))
    
    # Debug logging to see the final list of recommendations
    ai_api.logger.debug(f"Final recommendations: {recommendations}")

    # Return the recommendations as JSON
    return jsonify(recommendations)



# Running on port 8887
if __name__ == '__main__':
    # Set logging level to debug to show logs in the terminal
    ai_api.run(debug=True, port=8887)
