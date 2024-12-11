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

# Route for Noah's info with CORS applied
@ahaan_api.route('/api/noah', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_noah_info():
    return jsonify({
        "name": "Noah Harris",
        "age": 20,
        "city": "New York",
        "hobbies": ["football", "futsal", "soccer"]
    })

# Add more routes for other people as needed, with CORS applied
@ahaan_api.route('/api/person1', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_person1_info():
    return jsonify({
        "name": "Person One",
        "age": 22,
        "city": "Los Angeles",
        "hobbies": ["reading", "music", "traveling"]
    })

@ahaan_api.route('/api/person2', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_person2_info():
    return jsonify({
        "name": "Person Two",
        "age": 30,
        "city": "Chicago",
        "hobbies": ["sports", "movies", "music"]
    })

@ahaan_api.route('/api/person3', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_person3_info():
    return jsonify({
        "name": "Person Three",
        "age": 25,
        "city": "Austin",
        "hobbies": ["photography", "traveling", "art"]
    })

@ahaan_api.route('/api/person4', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_person4_info():
    return jsonify({
        "name": "Person Four",
        "age": 27,
        "city": "Seattle",
        "hobbies": ["gaming", "coding", "reading"]
    })

@ahaan_api.route('/api/person5', methods=['GET'])
@cross_origin()  # This allows CORS for this specific route
def get_person5_info():
    return jsonify({
        "name": "Person Five",
        "age": 28,
        "city": "Miami",
        "hobbies": ["music", "sports", "fitness"]
    })


