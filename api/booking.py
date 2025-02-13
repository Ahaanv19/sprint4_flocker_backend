from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from model.booking import db, Booking

# Blueprint setup for the API
booking_api = Blueprint('booking_api', __name__, url_prefix='/api')
api = Api(booking_api)

class BookAPI(Resource):
    def get(self):
        book = Booking.query.all()
        return jsonify([book.read() for book in book])  

    def post(self):
        data = request.get_json()
        if not data or 'title' not in data:
            return {'error': 'Title is required.'}, 400

        existing_book = Booking.query.filter_by(title=data['title']).first()
        if existing_book:
            return {'error': 'Book with this title already exists.'}, 400

        new_book = Booking(title=data['title'], genre=data.get('genre'), author=data.get('author'))
        result = new_book.create()  # Use the create method
        if result is None:
            return {'error': 'Error creating book.'}, 500

        return new_book.read(), 201  # Use the read method to return the book

    def put(self, book_id):
        data = request.get_json()
        if not data or 'title' not in data:
            return {'error': 'Title is required.'}, 400

        book = Booking.query.get(book_id)
        if not book:
            return {'error': 'Book not found.'}, 404

        book.title = data['title']
        if 'genre' in data:
            book.genre = data['genre']
        if 'author' in data:
            book.author = data['author']
        
        result = book.update(data)  # Pass the data to the update method
        if result is None:
            return {'error': 'Error updating book.'}, 500

        return book.read(), 200  # Use the read method to return the updated book

    def delete(self, book_id):
        book = Booking.query.get(book_id)
        if not book:
            return {'error': 'Book not found.'}, 404
        
        try:
            book.delete()  # Use the delete method from the model
        except Exception as e:
            return {'error': str(e)}, 500
        
        return {'message': 'Book deleted successfully.'}, 204

# Add the resource to the API
api.add_resource(BookAPI, '/book', '/book/<int:book_id>')