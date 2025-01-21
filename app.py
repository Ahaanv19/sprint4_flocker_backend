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
    # Create the `sections` table if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            _name TEXT NOT NULL UNIQUE,
            _theme TEXT
        )
    ''')

    # Insert static data related to books if it doesn't exist
    static_data = [
        ("Fiction", "Mystery"),
        ("Non-Fiction", "Educational"),
        ("Science Fiction", "Futuristic"),
        ("Fantasy", "Adventure"),
        ("Biography", "Inspiration")
    ]

    for name, theme in static_data:
        try:
            cursor.execute("INSERT INTO sections (_name, _theme) VALUES (?, ?)", (name, theme))
        except sqlite3.IntegrityError:
            # Ignore duplicates
            pass

    conn.commit()
    conn.close()

@app.route('/sections', methods=['GET', 'POST'])
def manage_sections():
    if request.method == 'GET':
        # Fetch all sections from the database
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sections")
            sections = [{"id": row[0], "name": row[1], "theme": row[2]} for row in cursor.fetchall()]
            conn.close()
            return jsonify(sections), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if request.method == 'POST':
        # Add a new section
        data = request.json
        name = data.get("name", "").strip()
        theme = data.get("theme", "").strip()

        if not name:
            return jsonify({"error": "Section name is required"}), 400

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sections (_name, _theme) VALUES (?, ?)", (name, theme))
            conn.commit()
            section_id = cursor.lastrowid
            conn.close()
            return jsonify({"id": section_id, "name": name, "theme": theme}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "Section name must be unique"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/sections/<int:section_id>', methods=['DELETE', 'PUT'])
def modify_section(section_id):
    if request.method == 'DELETE':
        # Delete a section by ID
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sections WHERE id = ?", (section_id,))
            conn.commit()
            conn.close()

            if cursor.rowcount == 0:
                return jsonify({"error": "Section not found"}), 404

            return jsonify({"message": "Section deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if request.method == 'PUT':
        # Edit a section by ID
        data = request.json
        name = data.get("name", "").strip()
        theme = data.get("theme", "").strip()

        if not name:
            return jsonify({"error": "Section name is required"}), 400

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("UPDATE sections SET _name = ?, _theme = ? WHERE id = ?", (name, theme, section_id))
            conn.commit()
            conn.close()

            if cursor.rowcount == 0:
                return jsonify({"error": "Section not found"}), 404

            return jsonify({"message": "Section updated successfully"}), 200
        except sqlite3.IntegrityError:
            return jsonify({"error": "Section name must be unique"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()  # Ensure the database and table are initialized
    app.run(port=3000, debug=True)
