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

# Route for Person 1's info
@ahaan_api.route('/api/noah', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_person1_info():
    return jsonify({
        "name": "noah",
        "age": 22,
        "city": "Los Angeles",
        "hobbies": ["reading", "music", "traveling"]
    })

# Route for Person 2's info
@ahaan_api.route('/api/arnav', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_arnav_info():
    return jsonify({
        "name": "Arnav",
        "age": 15,
        "city": "San Diego",
        "hobbies": ["sports", "videogames", "coding"]
    })

# Route for Person 3's info
@ahaan_api.route('/api/jacob', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_jacob_info():
    return jsonify({
        "name": "jacob",
        "age": 15,
        "city": "San Diego",
        "hobbies": ["gaming", "sports", "cooking"]
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

