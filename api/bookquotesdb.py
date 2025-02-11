from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.bookquotesdb import db, Quote  # Ensure you import the correct model

# Blueprint setup for the API
quotes_api = Blueprint('quotes_api', __name__, url_prefix='/api')
api = Api(quotes_api)

class QuoteAPI(Resource):
    def get(self):
        quotes = Quote.query.all()
        return jsonify([quote.read() for quote in quotes])

    def post(self):
        data = request.get_json()
        if not data or 'text' not in data:
            return {'error': 'Quote text is required.'}, 400

        new_quote = Quote(text=data['text'], book=data.get('book'), author=data.get('author'))
        result = new_quote.create()  # Use the create method
        if result is None:
            return {'error': 'Error creating quote.'}, 500

        return new_quote.read(), 201  # Use the read method to return the quote

    def put(self, quote_id):
        data = request.get_json()
        if not data or 'text' not in data:
            return {'error': 'Quote text is required.'}, 400

        quote = Quote.query.get(quote_id)
        if not quote:
            return {'error': 'Quote not found.'}, 404

        try:
            quote.update({'text': data['text'], 'book': data.get('book'), 'author': data.get('author')})  # Use the update method
        except Exception as e:
            return {'error': str(e)}, 500

        return quote.read(), 200  # Return the updated quote

    def delete(self, quote_id):
        quote = Quote.query.get(quote_id)
        if not quote:
            return {'error': 'Quote not found.'}, 404
        
        try:
            quote.delete()  # Use the delete method from the model
        except Exception as e:
            return {'error': str(e)}, 500
        
        return {'message': 'Quote deleted successfully.'}, 204

# Add the resource to the API
api.add_resource(QuoteAPI, '/quotes', '/quotes/<int:quote_id>')
