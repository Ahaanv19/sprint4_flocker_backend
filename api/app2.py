from flask import Blueprint, request, jsonify
from flask_cors import CORS
import sqlite3
import os

# Create a Blueprint for sections
app_bp = Blueprint('app_bp', __name__)

# Enable CORS for the Blueprint
CORS(app_bp)

# Path to the existing SQLite database
DB_PATH = './instance/volumes/user_management.db'

# Ensure the database file and table exist
def init_db():
    if not os.path.exists('./instance/volumes'):
        os.makedirs('./instance/volumes')

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usersDb (
            table_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            fav_book TEXT NOT NULL,
            user_id INTEGER NOT NULL UNIQUE
        )
    ''')

    # Insert static data if it doesn't exist
    static_data = [
        ("Arnav", "Maze Runner", 1),
        ("Ahaan", "Hunger Games", 2),
        ("John", "Example Book", 3)
    ]

    for name, fav_book, user_id in static_data:
        try:
            cursor.execute("INSERT INTO usersDb (name, fav_book, user_id) VALUES (?, ?, ?)", (name, fav_book, user_id))
        except sqlite3.IntegrityError:
            # Ignore duplicates
            pass

    conn.commit()
    conn.close()

@app_bp.route('/usersDb', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'GET':
        # Fetch all users from the database
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usersDb")
            users = [
                {"table_id": row[0], "name": row[1], "fav_book": row[2], "user_id": row[3]} 
                for row in cursor.fetchall()
            ]
            return jsonify(users), 200
        except Exception as e:
            return jsonify({"failed to fetch usersDb": str(e)}), 500
        finally:
            if 'conn' in locals():
                conn.close()

    if request.method == 'POST':
        try:
        # Add a new user
            data = request.json
            name = data.get("name", "").strip()
            fav_book = data.get("fav_book", "").strip()
            user_id = data.get("user_id")

            if not name or fav_book is None or user_id is None:
                return jsonify({"error": "Name, fav_book, and user_id are required"}), 400

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usersDb (name, fav_book, user_id) VALUES (?, ?, ?)", (name, fav_book, user_id))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return jsonify({"table_id": user_id, "name": name, "fav_book": fav_book, "user_id": user_id}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "User ID must be unique"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if 'conn' in locals():
                conn.close()

@app_bp.route('/usersDb/<int:user_id>', methods=['DELETE', 'PUT'])
def modify_user(user_id):
    if request.method == 'DELETE':
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usersDb WHERE user_id = ?", (user_id,))
            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({"error": "User not found"}), 404

            return jsonify({"message": "User deleted successfully"}), 200
        except Exception as e:
            return jsonify({"Failed to delete user": str(e)}), 500
        finally:
            if 'conn' in locals():
                conn.close()

    if request.method == 'PUT':
        try:
        # Update an existing user
            data = request.json
            name = data.get("name", "").strip()
            fav_book = data.get("fav_book", "").strip()

            if name is None and fav_book is None:
                return jsonify({"error": "At least one of name or fav_book must be provided"}), 400

            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("UPDATE sections SET _name = ?, _fav_book = ? WHERE user_id = ?", (name, fav_book, user_id))

            if cursor.rowcount == 0:
                return jsonify({"error": "User not found"}), 404

            return jsonify({"message": "User updated successfully"}), 200
        except sqlite3.IntegrityError:
            return jsonify({"error": "User name must be unique"}), 400
        except Exception as e:
            return jsonify({"error": f"Failed to update user: {e}"}), 500
        finally:
            if 'conn' in locals():
                conn.close()

# Initialize the database when the module is loaded
init_db()