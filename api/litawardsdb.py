# api/literaryawardsdb.py
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.litawardsdb import db, LiteraryAward  # Ensure you import the correct model

# Blueprint setup for the API
awards_api = Blueprint('awards_api', __name__, url_prefix='/api')
api = Api(awards_api)

class LiteraryAwardAPI(Resource):
    def get(self):
        awards = LiteraryAward.query.all()
        return jsonify([award.read() for award in awards])  

    def post(self):
        data = request.get_json()
        required_fields = ['book_title', 'award_name', 'year']
        if not all(field in data for field in required_fields):
            return {'error': 'Book title, award name, and year are required.'}, 400
        
        new_award = LiteraryAward(**data)
        result = new_award.create()  # Use the create method
        if result is None:
            return {'error': 'Error creating award entry.'}, 500

        return new_award.read(), 201  # Use the read method to return the award

    def put(self, award_id):
        award = LiteraryAward.query.get(award_id)
        if not award:
            return {'error': 'Award entry not found.'}, 404

        data = request.get_json()
        try:
            award.update(data)  # Use the update method
        except Exception as e:
            return {'error': str(e)}, 500

        return award.read(), 200  # Return the updated award

    def delete(self, award_id):
        award = LiteraryAward.query.get(award_id)
        if not award:
            return {'error': 'Award entry not found.'}, 404
        
        try:
            award.delete()  # Use the delete method from the model
        except Exception as e:
            return {'error': str(e)}, 500
        
        return {'message': 'Award entry deleted successfully.'}, 204

# Add the resource to the API
api.add_resource(LiteraryAwardAPI, '/awards', '/awards/<int:award_id>')
