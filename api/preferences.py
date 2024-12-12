from flask import Blueprint, jsonify, request
from flask_cors import cross_origin


preferences_api = Blueprint('preferences_api', __name__)


preferences = {
    "menu": "red",
    "text": "white"
}


# Route for Preferences info (GET)
@preferences_api.route('/api/preferences', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_preferences():
    return jsonify(preferences)


# Route to update Preferences (POST)
@preferences_api.route('/api/preferences', methods=['POST'])
@cross_origin()  # Allow CORS for this route
def update_preferences():
    # Check if the request contains JSON
    if request.is_json:
        # Get the new preferences data from the JSON body
        data = request.get_json()
       
        # Update preferences dictionary with the new data
        preferences.update(data)
       
        # Return the updated preferences as a response
        return jsonify(preferences), 200
    else:
        return jsonify({"error": "Request must be in JSON format"}), 400



