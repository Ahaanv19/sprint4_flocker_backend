# imports from flask
from flask import Blueprint, jsonify
from flask_restful import Api, Resource
student_api = Blueprint('student_api', __name__, url_prefix='/api')
# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(student_api)
class StudentAPI:
    @staticmethod
    def get_student(name):
        students = {
            "Jacob": {
                "name": "Jacob",
                "age": 5,
                "FavoriteBook": "asdfasd",            
            },
            "Noah": {
                "name": "Noah",
                "age": 16,
                "FavoriteBook": "Harry Potter and the Deathly Hallows", 
                "grade": 10,              
                "FavoriteNFLTeam" : "Detriot Lions",           
                },
            "Ahaan": {
                "name": "Ahaan",
                "age": 15,
                "grade" : 10,
            },
            "Arnav": {
                "name": "Arnav",
                "age": 15,
                "grade" : 10,
            }
        }
        return students.get(name)
    class _Jacob(Resource):
        def get(self):
            # Use the helper method to get Jacob's details
            jacob_details = StudentAPI.get_student("Jacob")
            return jsonify(jacob_details)
    class _Arnav(Resource):
        def get(self):
            # Use the helper method to get Jeff's details
            arnav_details = StudentAPI.get_student("Arnav")
            return jsonify(arnav_details)
    class _Noah(Resource):
        def get(self):
            # Use the helper method to get Jeff's details
            noah_details = StudentAPI.get_student("Noah")
            return jsonify(noah_details)
    class _Bulk(Resource):
        def get(self):
            # Use the helper method to get both John's and Jeff's details
            jacob_details = StudentAPI.get_student("Jacob")
            arnav_details = StudentAPI.get_student("Arnav")
            noah_details = StudentAPI.get_student("Noah")
            return jsonify({"students": [jacob_details, arnav_details, noah_details]})
    # Building REST API endpoints
    api.add_resource(_Jacob, '/student/jacob')
    api.add_resource(_Arnav, '/student/Arnav')
    api.add_resource(_Noah, '/student/Noah')
    api.add_resource(_Bulk, '/students')
# Instantiate the StudentAPI to register the endpoints
student_api_instance = StudentAPI()