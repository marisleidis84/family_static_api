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
    if request.method == 'GET':
        members = jackson_family.get_all_members()
        response_body = {
        "family": members
        }
        return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        if not request.json.get ('first_name'):
            return jsonify({"first_name": "is required"}), 404
        if not request.json.get ('age'):
            return jsonify({"age": "is required"}), 404
        if not request.json.get ('lucky_numbers'):
            return jsonify({"lucky_numbers": "is required"}), 404

        jackson_family.first_name = request.json.get('first_name')
        jackson_family.age = request.json.get('age')
        jackson_family.lucky_numbers = request.json.get('lucky_numbers')

        jackson_family.add_member(jackson_family)
        return jsonify({"result": "ok"}), 200

@app.route('/member/<int:id>', methods=['GET'])
def handle_member_get(id):

    if request.method == 'GET':
        member = jackson_family.get_member(id)
        if not member:
             return jsonify({"msg": "member not found"}), 400
        else:
            return jsonify(member), 200
    
@app.route('/member/<int:id>', methods=['PUT'])
def handle_member_update(id):
    if request.method == 'PUT':
        if not request.json.get ('first_name'):
            return jsonify({"first_name": "is required"}), 404
        if not request.json.get ('age'):
            return jsonify({"age": "is required"}), 404
        if not request.json.get ('lucky_numbers'):
            return jsonify({'lucky_numbers': 'is required'}), 404

    update = {
        "first_name": request.json.get("first_name"),
        "age": request.json.get("age"),
        "lucky_numbers": request.json.get("lucky_numbers")
    }

    jackson_family.update_member(id, update)
    return jsonify({"result": "ok"}), 200  

@app.route('/member/<int:id>', methods=['DELETE'])
def handle_member_delete(id):

    member = jackson_family.get_member(id)
    if member:
        jackson_family.delete_member(id)
        return jsonify({"msg": "member deleted ok"}), 200
    else:
        return jsonify({"msg": "member not found"}), 400
  
   


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
