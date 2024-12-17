# imports from flask
import json
import os
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, send_from_directory, url_for, jsonify, session  # import render_template from "public" flask libraries
from flask_login import current_user, login_user, logout_user
from flask.cli import AppGroup
from flask_login import current_user, login_required
from flask import current_app
from werkzeug.security import generate_password_hash
import shutil
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv

# import "objects" from "this" project
from __init__ import app, db, login_manager  # Key Flask objects 
# API endpoints
from api.user import user_api 
from api.pfp import pfp_api
from api.nestImg import nestImg_api # Justin added this, custom format for his website
from api.post import post_api
from api.channel import channel_api
from api.group import group_api
from api.section import section_api
from api.nestPost import nestPost_api # Justin added this, custom format for his website
from api.vote import vote_api
# database Initialization functions
from model.carChat import CarChat
from model.user import User, initUsers
from model.section import Section, initSections
from model.group import Group, initGroups
from model.channel import Channel, initChannels
from model.post import Post, initPosts
from model.nestPost import NestPost, initNestPosts # Justin added this, custom format for his website
from model.vote import Vote, initVotes

app.secret_key = os.urandom(24)  # Secret key for session management

# Load environment variables from .env file
load_dotenv(dotenv_path='/Users/jacobzierolf/nighthawk/sprint4_flocker_backend/password.env')

# Configure CORS to allow requests from your frontend
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:4887", "supports_credentials": True}})

# Initialize HTTP Basic Authentication
auth = HTTPBasicAuth()

# Define users and passwords
users = {
    os.getenv('ADMIN_USER'): os.getenv('ADMIN_PASSWORD'),
    os.getenv('DEFAULT_USER'): os.getenv('DEFAULT_PASSWORD')
}

# Verify password
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None

# Handle preflight requests
@app.before_request
def handle_options_requests():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = response.headers

        headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:4887'
        headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        headers['Access-Control-Allow-Credentials'] = 'true'

        return response

# Define a route for the root URL
@app.route('/')
def home():
    return 'Hello, World!'

# Define a login route with Basic Authentication
@app.route('/login', methods=['GET'])
@auth.login_required
def login():
    return jsonify({'message': 'Login successful', 'user': auth.current_user()})

# Define a logout route
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout successful'})

# Define a route to get user ID
@app.route('/api/id', methods=['GET'])
@auth.login_required
def get_id():
    user_id = {"id": 123}  # Example static ID, replace with actual logic if needed
    return jsonify(user_id)

# Define a route to get static data
@app.route('/api/staticData', methods=['GET'])
@auth.login_required
def get_data():
    staticData = ["data point 1", "data point 2", "data point 3"]
    return jsonify(staticData)

# Restore data to the new database
def restore_data(data):
    with app.app_context():
        users = User.restore(data['users'])
        _ = Section.restore(data['sections'])
        _ = Group.restore(data['groups'], users)
        _ = Channel.restore(data['channels'])
        _ = Post.restore(data['posts'])
    print("Data restored to the new database.")

# Define a command to backup data
@custom_cli.command('backup_data')
def backup_data():
    data = extract_data()
    save_data_to_json(data)
    backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])

# Define a command to restore data
@custom_cli.command('restore_data')
def restore_data_command():
    data = load_data_from_json()
    restore_data(data)

if __name__ == '__main__':
    app.run(port=8887, debug=True)


