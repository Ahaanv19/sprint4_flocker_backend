from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from model import user  # Ensure you have a User model set up to interact with the database

# Create Flask app and configure CORS
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing
api = Api(app)


class UserCRUD(Resource):
    def get(self):
        """
        Retrieve all users.

        Returns:
            JSON response with a list of all user names and IDs.
        """
        users = user.query.all()  # Retrieve all users from the database
        return jsonify([user.read() for user in users])

    def post(self):
        """
        Add a new user.

        Reads the 'name' field from the JSON request body and creates a new user.

        Returns:
            JSON response with the created user details or an error message.
        """
        body = request.get_json()
        name = body.get('name')

        if not name or len(name) < 2:
            return {'message': 'Name is required and must be at least 2 characters long'}, 400

        user = User(name=name)
        user = user.create()  # Save the user to the database

        if not user:
            return {'message': 'Failed to create user, possibly a duplicate name'}, 400

        return jsonify(user.read())

    def delete(self):
        """
        Delete a user.

        Deletes a user by 'id' provided in the JSON request body.

        Returns:
            A success message or an error message.
        """
        body = request.get_json()
        user_id = body.get('id')

        user = User.query.filter_by(id=user_id).first()

        if not user:
            return {'message': f'User with ID {user_id} not found'}, 404

        user_json = user.read()
        user.delete()  # Delete the user from the database

        return {'message': f"User {user_json['name']} deleted successfully"}, 200


# Register the resource with the API
api.add_resource(UserCRUD, '/users')

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
