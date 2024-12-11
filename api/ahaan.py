from flask import Blueprint, jsonify
from flask import Flask
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
        "name": "noah",
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
        "name": "jacob",
        "age": 15,
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


if __name__ == '__main__': # Ensures the code block is only ran if the script is run directly, not if it is imported as a module in another script
    app = Flask(__name__) # creates an instance of the Flask class. __name__ is a built-in Python variable that returns the name of the current module
    app.register_blueprint(ahaan_api) # Registers the blueprint with the Flask with the name ahaan_pi. Blueprints allow you to organize your Flask application by grouping routes together in a separate file
    app.run(debug=True, host="0.0.0.0", port=8887) # Runs the Flask application on the local development server. Debug=tru allows debug mode to provide a detailed error message and auto-reloads the server on code changes. host="0.0.0.0" allows the server to be accessible from any device on the network. Port=8887 specifies the port number to run the server on
