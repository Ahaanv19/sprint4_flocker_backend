from flask import Blueprint, request, jsonify
from flask_cors import CORS
import sqlite3
import os

# Create a Blueprint for sections
sections_bp = Blueprint('sections', __name__)

# Enable CORS for the Blueprint (Allow all origins for now)
CORS(sections_bp, resources={r"/*": {"origins": "https://ahaanv19.github.io"}})  # Apply CORS

# Path to the SQLite database
DB_PATH = './instance/volumes/user_management.db'

# Ensure the database file and table exist
def init_db():
    try:
        if not os.path.exists('./instance/volumes'):
            os.makedirs('./instance/volumes')

        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        # Create the sections table if it doesn't already exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                _name TEXT NOT NULL UNIQUE,
                _theme TEXT
            )
        ''')

        # Insert static data related to sections if it doesn't exist
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
                pass

        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

@sections_bp.route('/sections', methods=['GET', 'POST'])
def manage_sections():
    if request.method == 'GET':
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sections")
            sections = [{"id": row[0], "name": row[1], "theme": row[2]} for row in cursor.fetchall()]
            return jsonify(sections), 200
        except Exception as e:
            return jsonify({"error": f"Failed to fetch sections: {e}"}), 500
        finally:
            if 'conn' in locals():
                conn.close()

    if request.method == 'POST':
        try:
            data = request.get_json()
            name = data.get("name", "").strip()
            theme = data.get("theme", "").strip()

            if not name:
                return jsonify({"error": "Section name is required"}), 400

            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sections (_name, _theme) VALUES (?, ?)", (name, theme))
            conn.commit()
            section_id = cursor.lastrowid
            return jsonify({"id": section_id, "name": name, "theme": theme}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "Section name must be unique"}), 400
        except Exception as e:
            return jsonify({"error": f"Failed to add section: {e}"}), 500
        finally:
            if 'conn' in locals():
                conn.close()

@sections_bp.route('/sections/<int:section_id>', methods=['DELETE', 'PUT'])
def modify_section(section_id):
    if request.method == 'DELETE':
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sections WHERE id = ?", (section_id,))
            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({"error": "Section not found"}), 404

            return jsonify({"message": "Section deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to delete section: {e}"}), 500
        finally:
            if 'conn' in locals():
                conn.close()

    if request.method == 'PUT':
        try:
            data = request.get_json()
            name = data.get("name", "").strip()
            theme = data.get("theme", "").strip()

            if not name:
                return jsonify({"error": "Section name is required"}), 400

            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("UPDATE sections SET _name = ?, _theme = ? WHERE id = ?", (name, theme, section_id))
            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({"error": "Section not found"}), 404

            return jsonify({"message": "Section updated successfully"}), 200
        except sqlite3.IntegrityError:
            return jsonify({"error": "Section name must be unique"}), 400
        except Exception as e:
            return jsonify({"error": f"Failed to update section: {e}"}), 500
        finally:
            if 'conn' in locals():
                conn.close()

# Initialize the database when the module is loaded
init_db()