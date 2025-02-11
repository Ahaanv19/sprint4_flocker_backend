from flask import Blueprint, request, jsonify
from flask_cors import CORS

# Create the Blueprint with name `dewy_bp`
dewy_api = Blueprint("dewy_bp", __name__)  
CORS(dewy_api)  # Enable CORS for this blueprint

# In-memory storage (not a database)
users = []

@dewy_api.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@dewy_api.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if "name" not in data or "email" not in data:
        return jsonify({"error": "Missing name or email"}), 400

    new_user = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(new_user)
    return jsonify(new_user), 201

@dewy_api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": "User deleted"}), 200

@dewy_api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    for user in users:
        if user["id"] == user_id:
            user["name"] = data.get("name", user["name"])
            user["email"] = data.get("email", user["email"])
            return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404
