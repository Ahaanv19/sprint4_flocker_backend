from flask import Blueprint, jsonify, request
from flask_cors import CORS

user_api = Blueprint('user_api', __name__)
CORS(user_api)  # Enable CORS for this blueprint

# Dummy data to simulate a database
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

@user_api.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@user_api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@user_api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "Invalid input"}), 400
    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(new_user)
    return jsonify(new_user), 201

