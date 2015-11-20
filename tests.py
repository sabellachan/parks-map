import os
import unittest
from server import app, hash_password
from model import User, db
from flask import Flask
# from flask.ext.testing import TestCase
import datetime
# import tempfile


appkey = os.environ['appkey']
mapkey = os.environ['mapkey']
geocodekey = os.environ['geocodekey']


def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"
    db.app = app
    db.init_app(app)


class TestCase(unittest.TestCase):
    """Testing suite for server.py."""

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # set up fake test browser
        self.client = app.test_client()

        # connect to temporary database
        connect_to_db(app)

        # # create tables and add sample data
        db.create_all()

        # self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        # server.app.config['TESTING'] = True
        # self.app = server.app.test_client()
        # server.init_db()

    # def tearDown(self):
    #     os.close(self.db_fd)
    #     os.unlink(server.app.config['DATABASE'])

    def create_test_user(self):
        reg_date = datetime.datetime.now()

        test_user = User(reg_date=reg_date, email='test@user.com', password=hash_password('password'), first_name='John', last_name='Test', zipcode='94107')
        db.session.add(test_user)
        db.session.commit()

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

        test_client = app.test_client()
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

    # def test_process_login(self):
    #     """Tests to see if the login form will process properly with a known user."""

    #     # import pdb; pdb.set_trace()

    #     result = self.client.post("/process-login",
    #                             data={"email":'test@user.com', 'password':'password'},
    #                             follow_redirects=True)

    #     self.assertIn('Welcome back,', result.data)
    #     self.assertNotIn('Log In', result.data)
    #     self.assertNotIn('Please enter a valid email or password.', result.data)


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
