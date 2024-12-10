from flask import Blueprint, jsonify
from flask_cors import CORS

# Define the Blueprint
ahaan_api = Blueprint('ahaan_api', __name__)

# Enable CORS for this Blueprint
CORS(ahaan_api)

# Example endpoint
@ahaan_api.route('/api/ahaan', methods=['GET'])
def get_ahaan_info():
    return jsonify({
        "name": "Ahaan Vaidyanathan",
        "age": 15,
        "city": "San Diego",
        "hobbies": ["video games", "coding", "modeling"]
    })
