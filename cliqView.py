from flask import Blueprint, request, abort, jsonify
from flask.views import MethodView
from cliq import Cliq
from bson.objectid import ObjectId
import json
import datetime

cliq_view = Blueprint('cliq_view', __name__)

class CliqView(MethodView):

    def post(self):
        if not request.json:
            abort(400)
        if not Cliq.objects(cliq_id=request.json['cliq_id']).first == None:
            return jsonify({'Result':'Cliq ID already exists'})
        cliq = Cliq (
            cliq_id = request.json['cliq_id'],
            members = request.json['members'],
            bio = request.json['bio'],
            pending_members = request.json['pending_members'],
            last_active = datetime.datetime.now,
            _id = ObjectId()
        )
        cliq.save()
        return cliq.to_json()

    @cliq_view.route('/cliqs/<id>', methods=['GET'])
    def get(id):
        cliq = Cliq.objects(cliq_id=id).first()
        if cliq == None:
            return jsonify({'Result':'Cliq does not exist'})
        return cliq.to_json()

    @cliq_view.route('/cliqs/<id>', methods=['PUT'])
    def put(id):
        if not request.json:
            abort(400)
        cliq = Cliq.objects(cliq_id=id).first()
        if cliq == None:
            return jsonify({'Result':'Cliq does not exist'})
        if 'members' in request.json:
            user.update(members, request.json['members'])
        if 'bio' in request.json:
            user.update(bio, request.json['bio'])
        if 'pending_members' in request.json:
            user.update(pending_members, request.json['pending_members'])
        if 'last_active' in request.json:
            user.update(last_active, request.json['last_active'])
        cliq.save()
        return cliq.to_json()
    @cliq_view.route('/cliqs/<id>', methods=['DELETE'])
    def delete(id):
        cliq = Cliq.objects(cliq_id=id).first()
        if cliq == None:
            return jsonify({'Result':'Cliq does not exist'})
        cliq.delete()
        return jsonify({'Result':'Deleted'})

cliq_view.add_url_rule('/cliqs/', view_func=CliqView.as_view('cliqs'))
