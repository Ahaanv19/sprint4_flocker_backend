from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.bookadaptationsdb import db, Book  # Ensure you import the correct model

# Blueprint setup for the API
books_api = Blueprint('books_api', __name__, url_prefix='/api')
api = Api(books_api)

class BookAPI(Resource):
    def get(self):
        books = Book.query.all()
        return jsonify([book.read() for book in books])  

    def post(self):
        data = request.get_json()
        if not data or 'title' not in data:
            return {'error': 'Title is required.'}, 400

        existing_book = Book.query.filter_by(title=data['title']).first()
        if existing_book:
            return {'error': 'Book with this title already exists.'}, 400

        new_book = Book(title=data['title'])
        result = new_book.create()  # Use the create method
        if result is None:
            return {'error': 'Error creating book.'}, 500

        return new_book.read(), 201  # Use the read method to return the book

    def put(self, book_id):
        data = request.get_json()
        if not data or 'title' not in data:
            return {'error': 'Title is required.'}, 400

        book = Book.query.get(book_id)
        if not book:
            return {'error': 'Book not found.'}, 404

        try:
            book.update({'title': data['title']})  # Use the update method
        except Exception as e:
            return {'error': str(e)}, 500

        return book.read(), 200  # Return the updated book

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {'error': 'Book not found.'}, 404
        
        try:
            book.delete()  # Use the delete method from the model
        except Exception as e:
            return {'error': str(e)}, 500
        
        return {'message': 'Book deleted successfully.'}, 204

# Add the resource to the API
api.add_resource(BookAPI, '/books', '/books/<int:book_id>')