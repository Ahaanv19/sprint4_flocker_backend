from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Example API endpoint
@app.route('/api/ahaan', methods=['GET'])
def get_ahaan_info():
    return jsonify({
        "name": "Ahaan Vaidyanathan",
        "age": 15,
        "city": "San Diego",
        "hobbies": ["video games", "coding", "modeling"]
    })

if __name__ == '__main__':
    # Run the app
    app.run(debug=True, host="127.0.0.1", port=8887)

