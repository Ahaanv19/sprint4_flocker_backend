from flask import Flask, Blueprint, jsonify, request
from flask_cors import cross_origin

# Initialize Flask app
app = Flask(__name__)

crud_api = Blueprint('crud_api', __name__)

# In-memory storage for users
users = [{'name': 'Alice', 'uid': '1'}, {'name': 'Bob', 'uid': '2'}]

# Route to get all users (GET)
@crud_api.route('/api/crud', methods=['GET'])
@cross_origin()
def get_users():
    return jsonify(users), 200

# Route to create a new user (POST)
@crud_api.route('/api/crud', methods=['POST'])
@cross_origin()
def create_user():
    if request.is_json:
        data = request.get_json()
        if 'name' in data and 'uid' in data:
            new_user = {
                'name': data['name'],
                'uid': data['uid']
            }
            if any(user['uid'] == new_user['uid'] for user in users):
                return jsonify({"error": "User ID already exists."}), 409
            users.append(new_user)
            return jsonify(new_user), 201
        else:
            return jsonify({"error": "Request must contain 'name' and 'uid'"}), 400
    else:
        return jsonify({"error": "Request must be in JSON format"}), 400

# Route to delete a user (DELETE)
@crud_api.route('/api/crud/<string:user_id>', methods=['DELETE'])
@cross_origin()
def delete_user(user_id):
    user_to_delete = next((user for user in users if user['uid'] == user_id), None)
    if user_to_delete:
        users.remove(user_to_delete)  # Safer than reassigning the list
        return jsonify({"message": f"User with ID {user_id} deleted."}), 200
    else:
        return jsonify({"error": "User not found."}), 404

# Register the blueprint
app.register_blueprint(crud_api)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8887)
