from flask import Blueprint, request, jsonify
from flask_cors import CORS

# Create the Blueprint with name `dewy_api`
dewy_api = Blueprint("dewy_api", __name__)  

# Enable CORS for the Blueprint (Allow all origins for now)
CORS(dewy_api, resources={r"/*": {"origins": "https://ahaanv19.github.io"}})  # Apply CORS

# Static in-memory storage with predefined dewy data
dewy_data = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]

# Route to get all dewy data
@dewy_api.route('/dewy', methods=['GET'])
def get_dewy():
    return jsonify(dewy_data)

# Route to add new dewy data
@dewy_api.route('/dewy', methods=['POST'])
def add_dewy():
    data = request.get_json()
    if "name" not in data or "email" not in data:
        return jsonify({"error": "Missing name or email"}), 400

    new_dewy = {"id": len(dewy_data) + 1, "name": data["name"], "email": data["email"]}
    dewy_data.append(new_dewy)
    return jsonify(new_dewy), 201

# Route to delete a dewy entry
@dewy_api.route('/dewy/<int:dewy_id>', methods=['DELETE'])
def delete_dewy(dewy_id):
    global dewy_data
    dewy_data = [dewy for dewy in dewy_data if dewy["id"] != dewy_id]
    return jsonify({"message": "Dewy entry deleted"}), 200

# Route to update a dewy entry
@dewy_api.route('/dewy/<int:dewy_id>', methods=['PUT'])
def update_dewy(dewy_id):
    data = request.get_json()
    for dewy in dewy_data:
        if dewy["id"] == dewy_id:
            dewy["name"] = data.get("name", dewy["name"])
            dewy["email"] = data.get("email", dewy["email"])
            return jsonify(dewy), 200
    return jsonify({"error": "Dewy entry not found"}), 404
