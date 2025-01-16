from flask import Flask, Blueprint, jsonify, request
import random
from flask_cors import cross_origin
import json
import os
from flask import Blueprint, jsonify, request
from flask_cors import CORS


recomendations_api = Blueprint('ai_api', __name__)
CORS(recomendations_api)


@recomendations_api.route('/', methods=['GET']) ##test if the server is running correctly
@cross_origin() 
def home():
    return "Welcome to the Book Recomendations API!"

def load_books(): ##function to load the books from the json file (books.json)
    try:
        with open('books.json') as f:
            return json.load(f)
    except FileNotFoundError: ##if the file is not found return an error message
        return [], "File not found."
    except json.JSONDecodeError: 
        return [], "Error decoding JSON."
    
@recomendations_api.route('/recomendations', methods=['GET']) ##get all the books
@cross_origin() 
def get_books():
    books = load_books()
    return jsonify(books)
    
   
# Running on port 8887
if __name__ == '__main__':
    # Set logging level to debug to show logs in the terminal
    recomendations_api.run(debug=True, port=8887)
