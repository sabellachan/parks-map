import os
import unittest
import server
# from model import db
from flask import Flask
from flask.ext.testing import TestCase
# import tempfile

appkey = os.environ['appkey']
mapkey = os.environ['mapkey']
geocodekey = os.environ['geocodekey']


class TestCase(TestCase):
    """Testing suite for server.py."""

    # SQLALCHEMY_DATABASE_URI = "sqlite:///parks-test.db"
    # TESTING = True

    def setUp(self):
        self.client = server.app.test_client()
        # db.create_all()
        # self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        # server.app.config['TESTING'] = True
        # self.app = server.app.test_client()
        # server.init_db()

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    # def tearDown(self):
    #     db.session.remote()
    #     db.drop_all()
    #     os.close(self.db_fd)
    #     os.unlink(server.app.config['DATABASE'])

    #############################################################################
    # Test any functions that simply render a template.

    def test_load_homepage(self):
        """Tests to see if the index page comes up."""

        result = self.client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<h1>Parktake: <small>Cause the Outdoors Await</small></h1>', result.data)

    def test_load_signup(self):
        """Tests to see if the signup page comes up."""

        result = self.client.get('/signup')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Please register for an account.', result.data)

    def test_load_login(self):
        """Tests to see if the login page comes up."""

        result = self.client.get('/login')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Please log in.', result.data)

    def test_load_about(self):
        """Tests to see if the about page comes up."""

        result = self.client.get('/about')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Parktake was inspired by a love of adventure.', result.data)

    def test_load_logout(self):
        """Tests to see if logout occurs properly."""

        test_client = server.app.test_client()
        result = test_client.get('/logout')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<a id="nav-login" href="/login">Log In</a>', result.data)

    #############################################################################
    # Test any functions that will query data from the database.

    # def test_process_signup(self):  # UNSURE IF WORKS
    #     """Tests to see if the signup form will process properly."""

    #     result = self.client.post('/process-signup',
    #                               data={'first_name': "Jane",
    #                                     'last_name': "Smith",
    #                                     'zipcode': "94306",
    #                                     'email': "jane@jane.com",
    #                                     'password': 'password'},
    #                               follow_redirects=True)
    #     self.assertIn('<a href="/view-park" class="view-parks">Your Parks</a>', result.data)
    #     self.assertNotIn('<a id="nav-login" href="/login">Log In</a>', result.data)

        ## /process-login - use a known account + a fake account to test for if it works/not works ^^

    # def test_process_login(self):
    #     """Tests to see if the login form will process properly with a known user."""

    #     result = self.client.post('/process-login',
    #                               data={'email': 'test@test.com', 'password': 'n', 'mapkey': 'mapkey'},
    #                               follow_redirects=True)
    #     self.assertIn('Welcome back,', result.data)
    #     self.assertNotIn('Log In', result.data)


    #############################################################################
    # Test any functions that will request a JSON response

    # def test_parks_json(self):
    #     response = self.client.get("/parks.json")
    #     self.assertIsInstance(response, dict)

    # def test_visited_parks_json(self):
    #     response = self.client.get("/parks-visited.json")
    #     self.assertEquals(response.json, dict(success=True))


if __name__ == "__main__":
    unittest.main()
