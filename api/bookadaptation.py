from flask import Blueprint, jsonify, request
import json
import os

bookadaptation_api = Blueprint('bookadaptation_api', __name__)

def load_movies():  ##function to load the movies from the json file (movies.json)
    try:
        with open('movies.json') as f:
            return json.load(f)
    except FileNotFoundError:  ##if the file is not found return an error message
        return [], "File not found."
    except json.JSONDecodeError:
        return [], "Error decoding JSON."

@bookadaptation_api.route('/movies', methods=['GET'])  ##get all the movies
def get_movies():
    movies = load_movies()
    return jsonify(movies)

@bookadaptation_api.route('/movies/search', methods=['GET'])  # run something like http://localhost:5000/movies/search?title=1984 to check in postman (it works)
def search_movie():
    title = request.args.get('title')  ##get the title from the url
    movies = load_movies()

    # Find the movie by title (case-insensitive)
    found_movie = next((movie for movie in movies if movie['title'].lower() == title.lower()), None)

    if found_movie:  ##if the movie is found return it
        return jsonify(found_movie)
    else:
        return jsonify({'message': f'The movie "{title}" was not found.'}), 404

# Remove the home function since it's no longer needed.


##FIRST TEST