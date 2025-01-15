import logging
from flask import Flask, Blueprint, jsonify, request
import random
from flask_cors import cross_origin

# Initialize app and blueprint
app = Flask(__name__)
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
@cross_origin()  # Allow cross-origin requests
def recommendations():
    genre = request.args.get('genre', None)

    # Add logging to check if genre is being received correctly
    app.logger.debug(f"Received genre: {genre}")

    if genre:
        recommended_books = [book for book in books if book['genre'].lower() == genre.lower()]
        app.logger.debug(f"Filtered books by genre '{genre}': {recommended_books}")
    else:
        recommended_books = books
        app.logger.debug(f"No genre filter applied, all books: {recommended_books}")
    
    # Randomly select up to 3 books from the recommended list
    recommendations = random.sample(recommended_books, min(3, len(recommended_books)))
    
    # Log the final recommendations
    app.logger.debug(f"Final recommendations: {recommendations}")
    
    return jsonify(recommendations)

# Register blueprint with prefix '/api'
app.register_blueprint(ai_api, url_prefix='/api')

# Running on port 8887
if __name__ == '__main__':
    # Set logging level to debug to see the logs in the terminal
    app.debug = True
    app.run(debug=True, port=8887)
