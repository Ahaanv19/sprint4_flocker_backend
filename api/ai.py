from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

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

# AI book recommendation endpoint
@ai_api.route('/api/recommend', methods=['POST'])
def recommend_books():
    user_preferences = request.json.get('preferences', {})
    genre_preference = user_preferences.get('genre', None)
    
    if genre_preference:
        recommended_books = [book for book in books if book['genre'].lower() == genre_preference.lower()]
    else:
        recommended_books = books
    
    # Randomly select 3 books from the recommended list
    recommendations = random.sample(recommended_books, min(3, len(recommended_books)))
    
    return jsonify(recommendations)

# Register the blueprint with the Flask app
app.register_blueprint(ai_api)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)