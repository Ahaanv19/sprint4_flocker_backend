from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from model.booking import db, Booking

booking_api = Blueprint('booking_api', __name__, url_prefix='/api')
CORS(booking_api)
api = Api(booking_api)

class BookingAPI(Resource):
    def get(self):
        bookings = Booking.query.all()
        return jsonify([booking.read() for booking in bookings])

    def post(self):
        data = request.get_json()
        if not data or 'title' not in data or 'author' not in data or 'genre' not in data:
            return {'error': 'Title, author, and genre are required.'}, 400

        existing_book = Booking.query.filter_by(title=data['title']).first()
        if existing_book:
            return {'error': 'Book with this title already exists.'}, 400

        new_book = Booking(title=data['title'], author=data['author'], genre=data['genre'])
        result = new_book.create()
        if result is None:
            return {'error': 'Error creating book.'}, 500

        return new_book.read(), 201

    def put(self, book_id):
        data = request.get_json()
        if not data or 'title' not in data or 'author' not in data or 'genre' not in data:
            return {'error': 'Title, author, and genre are required.'}, 400

        book = Booking.query.get(book_id)
        if not book:
            return {'error': 'Book not found.'}, 404

        try:
            book.update({'title': data['title'], 'author': data['author'], 'genre': data['genre']})
        except Exception as e:
            return {'error': str(e)}, 500

        return book.read(), 200

    def delete(self, book_id):
        book = Booking.query.get(book_id)
        if not book:
            return {'error': 'Book not found.'}, 404

        try:
            book.delete()
        except Exception as e:
            return {'error': str(e)}, 500

        return {'message': 'Book deleted successfully.'}, 204

    def update_from_frontend(self):
        data = request.get_json()
        if not data or 'id' not in data or 'title' not in data or 'author' not in data or 'genre' not in data:
            return {'error': 'ID, title, author, and genre are required.'}, 400

        book = Booking.query.get(data['id'])
        if not book:
            return {'error': 'Book not found.'}, 404

        try:
            book.update({'title': data['title'], 'author': data['author'], 'genre': data['genre']})
        except Exception as e:
            return {'error': str(e)}, 500

        return book.read(), 200

api.add_resource(BookingAPI, '/book', '/book/<int:book_id>', '/book/update')