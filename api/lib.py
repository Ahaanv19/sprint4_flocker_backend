from flask import Blueprint, request, jsonify
from flask_cors import CORS

# Create the Blueprint with name `lib_api`
lib_api = Blueprint("lib_api", __name__)  

# Enable CORS for the Blueprint (Allow all origins for now)
CORS(lib_api, resources={r"/*": {"origins": "https://ahaanv19.github.io"}})  # Apply CORS

# Static in-memory storage with predefined library data
lib_data = [
    {"id": 1, "name": "San Diego County Library", "branch": "4S Ranch"},
    {"id": 2, "name": "San Diego County Library", "branch": "Rancho Santa Fe"},
    {"id": 3, "name": "San Diego Public Library", "branch": "Rancho Bernardo"}
]

# Route to get all library data
@lib_api.route('/lib', methods=['GET'])
def get_lib():
    return jsonify(lib_data)

# Route to add new library data
@lib_api.route('/lib', methods=['POST'])
def add_lib():
    data = request.get_json()
    if "name" not in data or "branch" not in data:
        return jsonify({"error": "Missing name or branch"}), 400

    new_lib = {"id": len(lib_data) + 1, "name": data["name"], "branch": data["branch"]}
    lib_data.append(new_lib)
    return jsonify(new_lib), 201

# Route to delete a library entry
@lib_api.route('/lib/<int:lib_id>', methods=['DELETE'])
def delete_lib(lib_id):
    global lib_data
    lib_data = [lib for lib in lib_data if lib["id"] != lib_id]
    return jsonify({"message": "Library entry deleted"}), 200

# Route to update a library entry
@lib_api.route('/lib/<int:lib_id>', methods=['PUT'])
def update_lib(lib_id):
    data = request.get_json()
    for lib in lib_data:
        if lib["id"] == lib_id:
            lib["name"] = data.get("name", lib["name"])
            lib["branch"] = data.get("branch", lib["branch"])
            return jsonify(lib), 200
    return jsonify({"error": "Library entry not found"}), 404

