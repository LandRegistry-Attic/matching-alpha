import unittest
import mock
import json
import uuid

from flask import jsonify

from matching import server
from matching.models import User, Role

user_data = {"name": "test",
            "date_of_birth": "1970-01-01",
            "gender" : "F",
            "current_address": "somewhere",
            "previous_address": "nowhere"}

user = User(**user_data)
lrid = uuid.uuid4()
user.lrid = lrid
citizen_role = Role(name="CITIZEN")
user.roles.append(citizen_role)

class MatchingTestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app
        self.client = self.app.test_client()

    def test_index_returns_ok(self):
        response = self.client.get('/')
        self.assertEquals(response.status, '200 OK')

    @mock.patch('matching.server._match_user', return_value=user)
    def test_matching_returns_lrid_of_matched_user(self, mock_match):
        with self.app.test_request_context():
            data = json.dumps(user_data)
            response = self.client.post('/match', data=data, content_type='application/json')

            expected = jsonify({"lrid": str(lrid), "roles": ["CITIZEN"]})
            self.assertEquals(response.status_code, 200)
            self.assertEquals(expected.data, response.data)

    @mock.patch('matching.server._match_user', return_value=None)
    def test_if_user_not_matched_return_404(self, mock_match):
        with self.app.test_request_context():
            data = json.dumps(user_data)
            response = self.client.post('/match', data=data, content_type='application/json')
            self.assertEquals(response.status_code, 404)

    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status, '200 OK')
