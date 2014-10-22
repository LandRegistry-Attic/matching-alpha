import json
import datetime
import uuid
import logging

from flask import current_app
from flask import request
from flask import Response
from flask import jsonify

from matching import app
from matching.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

app.logger.info("\nConfiguration\n%s\n" % app.config)

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
    # remove requirement for past address
    # for the moment so that we can use match for conveyancer/citizen
    # relationship. revisit this when IDA integration done. At that
    # time we may have matches with levels of assurance included?
    user = User.query.filter_by(name=name, gender=gender, current_address=current_address, date_of_birth=date_of_birth).first()

    current_app.logger.info('Matched user %s' % user)
    return user
