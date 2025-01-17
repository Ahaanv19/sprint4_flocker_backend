from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.bookadaptationsdb import NewBook

# Blueprint setup for the API
newbook_api = Blueprint('newbook_api', __name__, url_prefix='/api')
api = Api(newbook_api)

class BookAPI:
    """
    Define API endpoints for Book model.
    """
    class _CRUD(Resource):
        
        def post(self):
            """Create a new book."""
            data = request.get_json()
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'title' not in data or 'id' not in data:
                return {'message': 'Title and ID are required'}, 400
            
            try:
                book = NewBook(
                    title=data['title'],
                    id=data['id']
                )
                book.create()
                return jsonify({'message': 'Book created', 'book': book.read()}), 201
            except Exception as e:
                return {'message': f'Error creating book: {str(e)}'}, 500

        
        def get(self):
            """Retrieve all books."""
            try:
                books = NewBook.query.all()
                json_ready = [book.read() for book in books]
                return jsonify(json_ready), 200
            except Exception as e:
                return {'message': f'Error fetching books: {str(e)}'}, 500

        
        def put(self):
            """Update an existing book by its ID."""
            data = request.get_json()
            if 'id' not in data:
                return {'message': 'ID is required'}, 400

            book = NewBook.query.get(data['id'])
            if not book:
                return {'message': 'Book not found'}, 404

            try:
                book.update(data)
                return jsonify({'message': 'Book updated', 'book': book.read()}), 200
            except Exception as e:
                return {'message': f'Error updating book: {str(e)}'}, 500

        
        def delete(self):
            """Delete a book by its ID."""
            data = request.get_json()
            if 'id' not in data:
                return {'message': 'ID is required'}, 400

            book = NewBook.query.get(data['id'])
            if not book:
                return {'message': 'Book not found'}, 404

            try:
                book.delete()
                return jsonify({'message': 'Book deleted'}), 200
            except Exception as e:
                return {'message': f'Error deleting book: {str(e)}'}, 500

    # Add resource endpoints to API
    api.add_resource(_CRUD, '/books')  # Correct resource registration
