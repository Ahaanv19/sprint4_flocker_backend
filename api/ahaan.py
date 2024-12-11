from flask import Blueprint, jsonify
from flask_cors import cross_origin  # Import cross_origin for enabling CORS on individual routes

# Create a blueprint for all person-related APIs
ahaan_api = Blueprint('ahaan_api', __name__)

# Route for Ahaan's info
@ahaan_api.route('/api/ahaan', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_ahaan_info():
    return jsonify({
        "name": "Ahaan Vaidyanathan",
        "age": 15,
        "city": "San Diego",
        "hobbies": ["video games", "coding", "modeling"]
    })

# Route for Noah's info
@ahaan_api.route('/api/noah', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_person1_info():
    return jsonify({
        "name": "Noah Harris",
        "age": 16,
        "city": "El Cajon",
        "hobbies": ["football", "futsal", "videogames"]
    })

# Route for Person 2's info
@ahaan_api.route('/api/person2', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_person2_info():
    return jsonify({
        "name": "Person Two",
        "age": 28,
        "city": "Chicago",
        "hobbies": ["sports", "traveling", "cooking"]
    })

# Route for Person 3's info
@ahaan_api.route('/api/person3', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_person3_info():
    return jsonify({
        "name": "Person Three",
        "age": 30,
        "city": "Seattle",
        "hobbies": ["gaming", "hiking", "music"]
    })

# Route for Person 4's info
@ahaan_api.route('/api/person4', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_person4_info():
    return jsonify({
        "name": "Person Four",
        "age": 25,
        "city": "Austin",
        "hobbies": ["photography", "reading", "coding"]
    })

