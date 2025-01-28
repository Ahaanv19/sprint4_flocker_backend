from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Path to the existing SQLite database
DB_PATH = './instance/volumes/user_management.db'

# Ensure the database file and table exist
def init_db():
    if not os.path.exists('./instance/volumes'):
        os.makedirs('./instance/volumes')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usersDb (
            table_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            user_id INTEGER NOT NULL UNIQUE
        )
    ''')

    # Insert static data if it doesn't exist
    static_data = [
        ("Arnav", 15, 1),
        ("Ahaan", 15, 2),
        ("John", 3, 3)
    ]

    for name, age, user_id in static_data:
        try:
            cursor.execute("INSERT INTO usersDb (name, age, user_id) VALUES (?, ?, ?)", (name, age, user_id))
        except sqlite3.IntegrityError:
            # Ignore duplicates
            pass

    conn.commit()
    conn.close()

@app.route('/usersDb', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'GET':
        # Fetch all users from the database
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usersDb")
            users = [
                {"table_id": row[0], "name": row[1], "age": row[2], "user_id": row[3]} 
                for row in cursor.fetchall()
            ]
            conn.close()
            return jsonify(users), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if request.method == 'POST':
        # Add a new user
        data = request.json
        name = data.get("name", "").strip()
        age = data.get("age")
        user_id = data.get("user_id")

        if not name or age is None or user_id is None:
            return jsonify({"error": "Name, age, and user_id are required"}), 400

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usersDb (name, age, user_id) VALUES (?, ?, ?)", (name, age, user_id))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return jsonify({"table_id": user_id, "name": name, "age": age, "user_id": user_id}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "User ID must be unique"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/usersDb/<int:user_id>', methods=['DELETE', 'PUT'])
def modify_user(user_id):
    if request.method == 'DELETE':
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usersDb WHERE user_id = ?", (user_id,))
            conn.commit()
            rows_deleted = cursor.rowcount
            conn.close()

            if rows_deleted == 0:
                return jsonify({"error": "User not found"}), 404

            return jsonify({"message": "User deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if request.method == 'PUT':
        # Update an existing user
        data = request.json
        name = data.get("name")
        age = data.get("age")

        if name is None and age is None:
            return jsonify({"error": "At least one of name or age must be provided"}), 400

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Build the query dynamically based on provided fields
            query = "UPDATE usersDb SET "
            updates = []
            params = []

            if name is not None:
                updates.append("name = ?")
                params.append(name)

            if age is not None:
                updates.append("age = ?")
                params.append(age)

            query += ", ".join(updates) + " WHERE user_id = ?"
            params.append(user_id)

            cursor.execute(query, tuple(params))
            conn.commit()
            rows_updated = cursor.rowcount
            conn.close()

            if rows_updated == 0:
                return jsonify({"error": "User not found"}), 404

            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()  # Ensure the database and table are initialized
    app.run(port=3001, debug=True)