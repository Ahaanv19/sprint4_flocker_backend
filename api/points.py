from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

points_api = Blueprint('points_api', __name__)

points = 100  # Starting points

# Route to get points (GET)
@points_api.route('/api/points', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_points():
    return jsonify({"points": points})

# Route to update points (POST)
@points_api.route('/api/points', methods=['POST'])
@cross_origin()  # Allow CORS for this route
def update_points():
    global points
    if request.is_json:
        data = request.get_json()
        if 'points' in data:
            points = data['points']  # Update points with the new value
            return jsonify({"points": points}), 200
        else:
            return jsonify({"error": "Request must contain 'points'"}), 400
    else:
        return jsonify({"error": "Request must be in JSON format"}), 400

if __name__ == '__main__':
    points_api.run(debug=True, port=8887)
