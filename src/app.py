"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    family = jackson_family.get_all_members()
    return jsonify(family), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else: 
        return jsonify({
        "fail": "not a family member"
    }), 400

@app.route('/member', methods=['POST'])
def add_member():
    id = request.json.get('id')
    first_name = request.json.get('first_name')
    last_name = "Jackson"
    age = request.json.get('age')
    lucky_numbers = request.json.get('lucky_numbers')

    if not first_name:
        return jsonify({
            "message": "first name is required"
        }), 400
    if not last_name:
        return jsonify({
            "message": "last name is required"
        }), 400
    if not age:
        return jsonify({
            "message": "Age is required"
        }), 400
    if not lucky_numbers:
        return jsonify({
            "message": "Lucky numbers are required"
        }), 400
        
    member = {
        'first_name': first_name,
        'age': age,
        'lucky_numbers': lucky_numbers,
        'id': id
    }

    jackson_family.add_member(member)
    return jsonify({
        "success": "Family Member created"
        }), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.delete_member(member_id)
    if not member:
        return jsonify({
            "error": "not a family member"
        }), 400
    return jsonify(member)

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
