from flask import Blueprint, jsonify, request
from flask_cors import CORS

# Define the Blueprint for the chat API
chat_api = Blueprint('chat_api', __name__)
CORS(chat_api)  # Enable CORS for this blueprint

# Dummy data to simulate chat messages
chats = [
    {"id": 1, "sender": "Alice", "message": "Hi, Bob!", "timestamp": "2024-01-01 10:00:00"},
    {"id": 2, "sender": "Bob", "message": "Hi, Alice!", "timestamp": "2024-01-01 10:01:00"}
]

@chat_api.route('/chats', methods=['GET'])
def get_chats():
    """
    Retrieve all chat messages.
    """
    return jsonify(chats), 200

@chat_api.route('/chats/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    """
    Retrieve a single chat message by ID.
    """
    chat = next((c for c in chats if c['id'] == chat_id), None)
    if not chat:
        return jsonify({"error": "Chat not found"}), 404
    return jsonify(chat), 200

@chat_api.route('/chats', methods=['POST'])
def create_chat():
    """
    Create a new chat message.
    """
    data = request.json
    if not data or not data.get("sender") or not data.get("message"):
        return jsonify({"error": "Invalid input"}), 400
    new_chat = {
        "id": len(chats) + 1,
        "sender": data["sender"],
        "message": data["message"],
        "timestamp": data.get("timestamp", "2024-01-01 10:00:00")  # Default timestamp
    }
    chats.append(new_chat)
    return jsonify(new_chat), 201

