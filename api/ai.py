from flask import Blueprint, jsonify, request
import json
import os
from flask_cors import CORS, cross_origin

ai_api = Blueprint('ai_api', __name__)
CORS(ai_api)  ## Apply CORS globally to the Blueprint (optional, you can also apply it to individual routes)

def load_books():  ## Function to load the books from the JSON file (books.json)
    try:
        with open('books.json') as f:
            return json.load(f)
    except FileNotFoundError:  ## If the file is not found return an error message
        return [], "File not found."
    except json.JSONDecodeError:
        return [], "Error decoding JSON."

@ai_api.route('/recommendations', methods=['GET'])  ## Get all the books (recommendations)
@cross_origin()  ## Allow CORS on this specific route
def get_books():
    books = load_books()
    return jsonify(books)

# The home route is removed since it's not needed.

if __name__ == '__main__':
    ai_api.run(debug=True, port=8103)
