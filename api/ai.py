from flask import Blueprint, jsonify, request
import random

ai_api = Blueprint('ai_api', __name__)

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