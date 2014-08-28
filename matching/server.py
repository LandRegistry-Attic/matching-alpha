import json

from matching import app
from matching.models import User

@app.route('/')
def index():
    return "OK"


@app.route('/match', methods=['POST'])
def match():
    current_app.logger.info("Match request for json %s" % request.json)
    data = json.loads(request.json)
    current_app.logger.info("DATA %s" % data)
    return "OK"
