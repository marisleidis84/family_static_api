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
app.config['ENV'] = 'developnent'
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
def handle_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/members/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def handle_member(id = None):
    if request.method == 'GET':
        member = jackson_family
        if id > len(member._members):
            return jsonify({"msg": "member not found"}), 404
        return jsonify(member.get_member(id)), 200
    
    if request.method == 'DELETE':
        pass

@app.route('/members', methods=['POST'])
def handle_add():
   if request.method == 'POST':
        if not request.json.get ('first_name'):
            return jsonify({"first_name": "is required"}), 422
        if not request.json.get ('age'):
            return jsonify({"age": "is required"}), 422
        if not request.json.get ('lucky_numbers'):
            return jsonify({"lucky_numbers": "is required"}), 422

        jackson_family.first_name = request.json.get('first_name')
        jackson_family.age = request.json.get('age')
        jackson_family.lucky_numbers = request.json.get('lucky_numbers')

        member = jackson_family.add_member(jackson_family)
        return jsonify(member), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
