import unittest

from matching import server

class MatchingTestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def test_index_returns_ok(self):
        response = self.app.get('/')
        self.assertEquals(response.status, '200 OK')
