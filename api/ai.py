from flask import Blueprint, jsonify, request
import json
import os
from flask_cors import CORS, cross_origin

ai_api = Blueprint('ai_api', __name__)
CORS(ai_api) ##to allow the frontend to access the API


@ai_api.route('/', methods=['GET']) ##test if the server is running correctly
@cross_origin() 
def home():
    return "Welcome to the Book Adaptations API!"

def load_books(): ##function to load the movies from the json file (movies.json)
    try:
        with open('books.json') as f:
            return json.load(f)
    except FileNotFoundError: ##if the file is not found return an error message
        return [], "File not found."
    except json.JSONDecodeError: 
        return [], "Error decoding JSON."
    
@ai_api.route('/recommendations', methods=['GET']) ##get all the movies
@cross_origin() 
def get_books():
    books = load_books()
    return jsonify(books)

if __name__ == '__main__':
    ai_api.run(debug=True, port=8103)