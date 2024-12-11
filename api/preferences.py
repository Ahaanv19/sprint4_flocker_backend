from flask import Blueprint, jsonify
from flask_cors import cross_origin

preferences_api = Blueprint('preferences_api', __name__)

preferences = {
    "background": "blue",
    "menu" : "red",
    "text" : "white"
}

# Route for Preferences info
@preferences_api.route('/api/preferences', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_preferences():
    return jsonify(preferences)