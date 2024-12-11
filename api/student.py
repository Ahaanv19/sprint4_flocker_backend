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
                "FirstName": "Jacob",
                "LastName": "Zierof",
                "DOB": "who cares",
                "age": 5,
                "FavoriteBook": "asdfasd",            
            },
            "NoahJohny": {
                "FirstName": "ohnyNoah",
                "LastName": "Harris",
                "DOB": "March 9",
                "age": 16,
                "FavoriteBook": "Harry Potter and the",                
                "FavoriteNFLTeam" : "Detriot Lions",           
                },
            "Ahaan": {
                "name": "Ahaan",
                "age": 15,
                "major": "N/A",
                "university": "N/A",
                "grade" : 10,
                "DOB" : "May 19"
            },
            "Arnav": {
                "name": "Arnav",
                "age": 15,
                "major": "N/A",
                "university": "N/A",
                "grade" : 10,
                "DOB" : "June 25"
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
    class _Bulk(Resource):
        def get(self):
            # Use the helper method to get both John's and Jeff's details
            jacob_details = StudentAPI.get_student("Jacob")
            johny_details = StudentAPI.get_student("Johny")
            return jsonify({"students": [jacob_details, johny_details]})
    # Building REST API endpoints
    api.add_resource(_Jacob, '/student/jacob')
    api.add_resource(_Arnav, '/student/johny')
    api.add_resource(_Bulk, '/students')
# Instantiate the StudentAPI to register the endpoints
student_api_instance = StudentAPI()