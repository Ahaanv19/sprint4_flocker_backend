from flask import Blueprint, jsonify, request
from flask_cors import CORS

post_api = Blueprint('post_api', __name__)
CORS(post_api)  # Enable CORS for this blueprint

# Dummy data to simulate a database
posts = [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."}
]

@post_api.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts), 200

@post_api.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post), 200

@post_api.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "Invalid input"}), 400
    new_post = {
        "id": len(posts) + 1,
        "title": data["title"],
        "content": data["content"]
    }
    posts.append(new_post)
    return jsonify(new_post), 201

