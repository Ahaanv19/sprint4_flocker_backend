from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS  # Import CORS
from model.mod import Section

section_api = Blueprint('section_api', __name__, url_prefix='/api')
CORS(section_api, resources={r"/*": {"origins": "https://ahaanv19.github.io"}})  # Apply CORS

api = Api(section_api)

class SectionAPI:
    class _CRUD(Resource):
        def post(self):
            data = request.get_json()
            section = Section(data['name'], data['theme'])
            section.create()
            return jsonify(section.read())

        def get(self):
            sections = Section.query.all()
            return jsonify([section.read() for section in sections])

        def put(self):
            data = request.get_json()
            section = Section.query.get(data['id'])
            if section:
                section.update(data)
                return jsonify(section.read())
            return jsonify({'message': 'Section not found'}), 404

        def delete(self):
            data = request.get_json()
            section = Section.query.get(data['id'])
            if section:
                section.delete()
                return jsonify({'message': 'Section deleted'})
            return jsonify({'message': 'Section not found'}), 404

api.add_resource(SectionAPI._CRUD, '/section')
