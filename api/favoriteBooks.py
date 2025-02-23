from flask import Blueprint, request
from flask_restful import Api, Resource
from model.favoriteBooks import db, FavoriteBook

# Blueprint setup for the API
favbook_api = Blueprint('favbook_api', __name__, url_prefix='/api')
api = Api(favbook_api)

class FavoriteBookListAPI(Resource):
    """Handles GET (list all) and POST (add new book)"""
    
    def get(self):
        favorite_books = FavoriteBook.query.all()
        return {"books": [book.read() for book in favorite_books]}, 200  

    def post(self):
        data = request.get_json()
        if not data or 'title' not in data:
            return {'error': 'Title is required.'}, 400

        existing_favorite_book = FavoriteBook.query.filter_by(title=data['title']).first()
        if existing_favorite_book:
            return {'error': 'Book with this title already exists.'}, 400

        new_favorite_book = FavoriteBook(title=data['title'])
        db.session.add(new_favorite_book)
        db.session.commit()  # Save to database

        return new_favorite_book.read(), 201  

class FavoriteBookDetailAPI(Resource):
    """Handles GET (fetch one), PUT (update), and DELETE (remove)"""
    
    def put(self, favorite_book_id):
        data = request.get_json()
        if not data or 'title' not in data:
            return {'error': 'Title is required.'}, 400

        favorite_book = FavoriteBook.query.get(favorite_book_id)
        if not favorite_book:
            return {'error': 'Book not found.'}, 404

        favorite_book.title = data['title']
        db.session.commit()  # Save update to database

        return favorite_book.read(), 200  

    def delete(self, favorite_book_id):
        favorite_book = FavoriteBook.query.get(favorite_book_id)
        if not favorite_book:
            return {'error': 'Book not found.'}, 404
        
        db.session.delete(favorite_book)
        db.session.commit()  # Remove from database
        
        return {'message': 'Book deleted successfully.'}, 200  

# Add the resources to the API with proper routes
api.add_resource(FavoriteBookListAPI, '/favorite_books')  # Handles list and add
api.add_resource(FavoriteBookDetailAPI, '/favorite_books/<int:favorite_book_id>')  # Handles update and delete
