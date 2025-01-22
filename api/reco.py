from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.reco import Recommendation
from __init__ import db

reco_api = Blueprint('reco_api', __name__, url_prefix='/api')
api = Api(reco_api)

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