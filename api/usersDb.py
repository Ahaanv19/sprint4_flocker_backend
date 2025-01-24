from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.usersDb import usersDb

# Blueprint setup for the API
usersDb_api = Blueprint('usersDb_api', __name__, url_prefix='/api')
api = Api(usersDb_api)

class usersDbAPI:
    """
    Define API endpoints for UserCreation model.
    """
    class _CRUD(Resource):
        @token_required
        def post(self):
            """
            Create a new user.
            """
            data = request.get_json()
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'name' not in data or 'age' not in data or 'user_id' not in data:
                return {'message': 'Name, age, and user_id are required'}, 400

            try:
                user = usersDb(
                    name=data['name'],
                    age=data['age'],
                    user_id=data['user_id']
                )
                user.create()
                return jsonify({'message': 'User created', 'user': user.read()}), 201
            except Exception as e:
                return {'message': f'Error creating user: {str(e)}'}, 500

        @token_required
        def get(self):
            """
            Retrieve all users.
            """
            try:
                users = usersDb.query.all()
                json_ready = [user.read() for user in users]
                return jsonify(json_ready), 200
            except Exception as e:
                return {'message': f'Error fetching users: {str(e)}'}, 500

        @token_required
        def put(self):
            """
            Update an existing user by its ID.
            """
            data = request.get_json()
            if 'id' not in data:
                return {'message': 'ID is required'}, 400

            user = usersDb_api.query.get(data['id'])
            if not user:
                return {'message': 'user not found'}, 404

            try:
                user.update(data)
                return jsonify({'message': 'user updated', 'user': user.read()}), 200
            except Exception as e:
                return {'message': f'Error updating user: {str(e)}'}, 500

        @token_required
        def delete(self):
            """
            Delete a user by its ID.
            """
            data = request.get_json()
            if 'id' not in data:
                return {'message': 'ID is required'}, 400

            user = usersDb_api.query.get(data['id'])
            if not user:
                return {'message': 'user not found'}, 404

            try:
                user.delete()
                return jsonify({'message': 'user deleted'}), 200
            except Exception as e:
                return {'message': f'Error deleting user: {str(e)}'}, 500

    # Add resource endpoints to API
    api.add_resource(_CRUD, '/user')  # Routes for single user creation, update, get, and delete