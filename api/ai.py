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

@ai_api.route("/check", methods=["GET"])
@cross_origin() 
def home():
    return "Welcome to the AI API!"

# Endpoint to get book recommendations
@ai_api.route('/recommendations', methods=['GET'])
def recommendations():
    # Get the genre or query from the user
    genre = request.args.get('genre', None)
    
    # Filter books based on the genre
    if genre:
        recommended_books = [book for book in books if book['genre'].lower() == genre.lower()]
    else:
        recommended_books = books
    
    # Randomly select up to 3 books from the recommended list
    recommendations = random.sample(recommended_books, min(3, len(recommended_books)))
    
    return jsonify(recommendations)


# Running on port 8887
if __name__ == '__main__':
    # Set logging level to debug to show logs in the terminal
    ai_api.run(debug=True, port=8887)
