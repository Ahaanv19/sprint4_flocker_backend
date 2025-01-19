from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from model.bookadaptationsdb import db, Book  # Ensure you import the correct model

# Blueprint setup for the API
books_api = Blueprint('books_api', __name__, url_prefix='/api')
CORS(books_api)
api = Api(books_api)

class BookAPI(Resource):
    def get(self):
        books = Book.query.all()  # Use Book.query.all() to get all books
        return jsonify([book.serialize() for book in books])  # Serialize each book
        
    def post(self):
        data = request.get_json()  # Get the posted data
        new_book = Book(  # Create a new Book instance
            title=data['title'],
        )
        db.session.add(new_book)  # Add the new book to the session
        db.session.commit()  # Commit the changes to the database
        return jsonify(new_book.serialize()), 201  # Return the newly created book

# Add the resource to the API
api.add_resource(BookAPI, '/books')
