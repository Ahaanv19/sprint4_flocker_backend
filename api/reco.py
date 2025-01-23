from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import cross_origin, CORS
from model.reco import initRecommendations, Recommendation, add_book_to_db, db, Book
from __init__ import db

reco_api = Blueprint('reco_api', __name__, url_prefix='/api')
api = Api(reco_api)
CORS(reco_api)

class RecommendationAPI(Resource):
    def get(self):
        recommendations = Recommendation.query.all()
        return jsonify([rec.read() for rec in recommendations])

    def post(self):
        data = request.get_json()
        if not data or 'title' not in data or 'author' not in data or 'genre' not in data:
            return {'error': 'Title, author, and genre are required.'}, 400

        new_recommendation = Recommendation(
            title=data['title'],
            author=data['author'],
            genre=data['genre']
        )
        new_recommendation.create()
        return new_recommendation.read(), 201

api.add_resource(RecommendationAPI, '/recommendations')

@reco_api.route('/books', methods=['POST'])
@cross_origin()
def add_book():
    new_book = request.json
    try:
        added_book = add_book_to_db(new_book)
        return jsonify({
            'id': added_book.id,
            'title': added_book.title,
            'author': added_book.author,
            'genre': added_book.genre
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500