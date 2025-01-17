from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle CORS errors

# Initialize Flask app
app = Flask(__name__)

# Allow all origins to make requests to this server
CORS(app)

# In-memory user data for simplicity (could be replaced with a database)
users = [
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Jane Smith"}
]

# Route to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Route to add a user
@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.get_json()  # Get the data from the request
    if not new_user or 'name' not in new_user:
        return jsonify({'error': 'Name is required'}), 400

    # Generate the next user ID
    new_user['id'] = max(user['id'] for user in users) + 1
    users.append(new_user)
    return jsonify(new_user), 201

# Route to delete a user
@app.route('/users', methods=['DELETE'])
def delete_user():
    user_id = request.get_json().get("id")
    if not user_id:
        return jsonify({"error": "ID is required"}), 400
    
    global users
    # Find and remove the user with the given ID
    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": f"User {user_id} deleted successfully"}), 200

# Run the app on port 3000
if __name__ == '__main__':
    app.run(debug=True, port=3000)
