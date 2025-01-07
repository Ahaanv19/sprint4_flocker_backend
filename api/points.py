from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

points_api = Blueprint('points_api', __name__)

points = 10

# Route for Preferences info (GET)
@points_api.route('/api/points', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_points():
    return jsonify({"points": points})

# Route to update Preferences (POST)
@points_api.route('/api/points', methods=['POST'])
@cross_origin()  # Allow CORS for this route
def update_points():
    # Check if the request contains JSON
    if request.is_json:
        # Get the new points data from the JSON body
        data = request.get_json()

        # Check if the data contains 'points' to update
        if 'points' in data:
            global points  # Declare 'points' as global to modify it
            points = data['points']  # Update the points with the new value
            return jsonify({"points": points}), 200
        else:
            return jsonify({"error": "Request must contain 'points'"}), 400
    else:
        return jsonify({"error": "Request must be in JSON format"}), 400
