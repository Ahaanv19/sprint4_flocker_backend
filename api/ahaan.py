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
        "hobbies": ["futsal", "football", "gaming"]
    })


# Route for Arnav's info
@ahaan_api.route('/api/arnav', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_arnav_info():
    return jsonify({
        "name": "Arnav",
        "age": 15,
        "city": "San Diego",
        "hobbies": ["sports", "videogames", "coding"]
    })

# Route for Jacob's info
@ahaan_api.route('/api/jacob', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_jacob_info():
    return jsonify({
        "name": "Jacob",
        "age": 16,
        "city": "San Diego",
        "hobbies": ["gaming", "sports", "cooking"]
    })

# Route for James's info
@ahaan_api.route('/api/james', methods=['GET'])
@cross_origin()  # Allow CORS for this route
def get_person4_info():
    return jsonify({
        "name": "James Edrosolo",
        "age": 15,
        "city": "San Diego",
        "hobbies": ["wrestling", "working out", "eating"]
    })
