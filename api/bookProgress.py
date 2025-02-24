from flask import Blueprint, request
from flask_restful import Api, Resource
from model.bookProgress import db, BookProgress

# Blueprint setup for the API
book_progress_api = Blueprint('book_progress_api', __name__, url_prefix='/api')
api = Api(book_progress_api)

class BookProgressListAPI(Resource):
    """Handles GET (list all) and POST (add new book progress)"""
    
    def get(self):
        book_progress_list = BookProgress.query.all()
        return {"books": [book.read() for book in book_progress_list]}, 200  

    def post(self):
        data = request.get_json()
        if not data or 'title' not in data:
            return {'error': 'Title is required.'}, 400

        existing_book_progress = BookProgress.query.filter_by(title=data['title']).first()
        if existing_book_progress:
            return {'error': 'Book with this title already exists.'}, 400

        new_book_progress = BookProgress(title=data['title'], percent_read=data.get('percent_read', 0.0))
        db.session.add(new_book_progress)
        db.session.commit()  # Save to database

        return new_book_progress.read(), 201  

class BookProgressDetailAPI(Resource):
    """Handles GET (fetch one), PUT (update), and DELETE (remove)"""
    
    def put(self, book_progress_id):
        data = request.get_json()
        if not data or 'title' not in data:
            return {'error': 'Title is required.'}, 400

        book_progress = BookProgress.query.get(book_progress_id)
        if not book_progress:
            return {'error': 'Book progress not found.'}, 404

        book_progress.title = data['title']
        book_progress.percent_read = data.get('percent_read', book_progress.percent_read)
        db.session.commit()  # Save update to database

        return book_progress.read(), 200  

    def delete(self, book_progress_id):
        book_progress = BookProgress.query.get(book_progress_id)
        if not book_progress:
            return {'error': 'Book progress not found.'}, 404
        
        db.session.delete(book_progress)
        db.session.commit()  # Remove from database
        
        return {'message': 'Book progress deleted successfully.'}, 200  

# Add the resources to the API with proper routes
api.add_resource(BookProgressListAPI, '/book_progress')  # Handles list and add
api.add_resource(BookProgressDetailAPI, '/book_progress/<int:book_progress_id>')  # Handles update and delete