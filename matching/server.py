import json
import datetime
import uuid

from flask import current_app
from flask import request
from flask import Response
from flask import jsonify

from matching import app
from matching.models import User

@app.route('/')
def index():
    return "OK"

@app.route('/match', methods=['POST'])
def match():
    current_app.logger.info("Match requested for %s" % request.get_json())
    user = _match_user(**request.get_json())
    if user:
        user_roles = [item.name for item in user.roles]
        return jsonify({"lrid": str(user.lrid), "roles": user_roles})
    else:
        return Response(json.dumps({"status": "not found"}), status = 404, mimetype='application/json')


def _match_user(**kwargs):
    name = kwargs['name']
    date_of_birth = datetime.datetime.strptime(kwargs['date_of_birth'], '%Y-%m-%d')
    gender = kwargs['gender']
    current_address = kwargs['current_address']
    previous_address = kwargs['previous_address']

    user = User.query.filter_by(name=name, gender=gender, current_address=current_address, previous_address=previous_address, date_of_birth=date_of_birth).first()

    current_app.logger.info('Matched user %s' % user)
    return user
