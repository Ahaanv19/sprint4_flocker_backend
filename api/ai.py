import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Your Google Books API Key
API_KEY = 'AIzaSyBwiIaFOgmnzkOTD-HwegvolORp2rx1Lfk'

# Function to search books via Google Books API
def search_books(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Could not fetch data from Google Books API"}

# Endpoint to get book recommendations
@app.route('/recommendations', methods=['GET'])
def recommendations():
    # Get the genre or query from the user
    genre = request.args.get('genre', 'programming')  # Default to 'programming' if no genre is provided
    
    # Call the function to fetch books
    books_data = search_books(genre)
    
    # Process the response and return relevant details
    recommendations = []
    if 'items' in books_data:
        for item in books_data['items']:
            book_info = item['volumeInfo']
            book = {
                "title": book_info.get("title"),
                "authors": book_info.get("authors", []),
                "description": book_info.get("description", "No description available"),
                "rating": book_info.get("averageRating", "No rating"),
                "thumbnail": book_info.get("imageLinks", {}).get("thumbnail", ""),
                "infoLink": book_info.get("infoLink")
            }
            recommendations.append(book)
    
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
