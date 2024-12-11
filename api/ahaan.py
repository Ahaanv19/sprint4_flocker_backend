from flask import Blueprint, jsonify
from flask_cors import cross_origin  # Import cross_origin for specific routes

# Create a blueprint for all person-related APIs
ahaan_api = Blueprint('ahaan_api', __name__)

# Apply CORS for specific route
@ahaan_api.route('/api/ahaan', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_ahaan_info():
    return jsonify({
        "name": "Ahaan Vaidyanathan",
        "age": 15,
        "city": "San Diego",
        "hobbies": ["video games", "coding", "modeling"]
    })

# Route for Person 1 info 
@ahaan_api.route('/api/person1', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_person1_info():
    return jsonify({
        "name": "Person One",
        "age": 20,
        "city": "New York",
        "hobbies": ["football", "futsal", "soccer"]
    })

# Route for Person 2
@ahaan_api.route('/api/person2', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_person2_info():
    return jsonify({
        "name": "Person Two",
        "age": 30,
        "city": "Chicago",
        "hobbies": ["sports", "movies", "music"]
    })

# Route for Person 3
@ahaan_api.route('/api/person3', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_person3_info():
    return jsonify({
        "name": "Person Three",
        "age": 25,
        "city": "Austin",
        "hobbies": ["photography", "traveling", "art"]
    })

# Route for Person 4
@ahaan_api.route('/api/person4', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_person4_info():
    return jsonify({
        "name": "Person Four",
        "age": 27,
        "city": "Seattle",
        "hobbies": ["gaming", "coding", "reading"]
    })
