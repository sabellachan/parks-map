import os
import unittest
from server import app, get_parks
from model import db, connect_to_db, example_data_rec_areas, example_data_users, example_data_visits
from flask import Flask, session

appkey = os.environ['appkey']
mapkey = os.environ['mapkey']
geocodekey = os.environ['geocodekey']


class ParkTests(unittest.TestCase):
    """Testing suite for server.py."""

    def setUp(self):
        # set up fake test browser
        self.client = app.test_client()

        # connect to temporary database
        connect_to_db(app, "sqlite:///")

        # This line makes a 500 error in a route raise an error in a test
        app.config['TESTING'] = True

        # # create tables and add sample data
        db.create_all()
        example_data_rec_areas()
        example_data_users()
        example_data_visits()

#############################################################################
# Test any functions that only render a template.

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

    def test_load_landing(self):
        """Tests to see if the landing page comes up."""  # CURRENTLY RETURNS 500 ERROR

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = '2'
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            result = c.get('/landing', data={'mapkey': mapkey}, follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Your Parks', result.data)

    def test_load_logout(self):
        """Tests to see if logout occurs properly."""

        result = self.client.get('/logout')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<a id="nav-login" href="/login">Log In</a>', result.data)

#############################################################################
# Test any functions that will query data or require a session.

    def test_process_signup_new_user(self):
        """Test to see if the signup form will process new user properly."""

        result = self.client.post('/process-signup',
                                  data={'first_name': "Jane",
                                        'last_name': "Smith",
                                        'zipcode': "94306",
                                        'email': "jane@jane.com",
                                        'password': 'password'},
                                  follow_redirects=True)
        self.assertIn('<a href="/view-park" class="view-parks">Your Parks</a>', result.data)
        self.assertNotIn('<a id="nav-login" href="/login">Log In</a>', result.data)

    def test_process_signup_known_user(self):
        """Test to see if the signup form will process a user currently in the database properly."""

        result = self.client.post('/process-signup',
                                  data={'first_name': "Jane",
                                        'last_name': "Smith",
                                        'zipcode': "94306",
                                        'email': "admin@maynard.com",
                                        'password': 'password'},
                                  follow_redirects=True)
        self.assertIn('/login', result.data)
        self.assertNotIn('Welcome, ', result.data)

    def test_process_login_known(self):
        """Test to see if the login form will process properly with a known user."""

        result = self.client.post("/process-login",
                                  data={"email": 'lucy@test.com', 'password': 'brindlepuppy'},
                                  follow_redirects=True)

        self.assertIn('Welcome back,', result.data)
        self.assertNotIn('Log In', result.data)
        self.assertNotIn('Please enter a valid email or password.', result.data)

    def test_process_login_unknown(self):
        """Test to see if the login form will process properly with an unknown user."""

        result = self.client.post("/process-login",
                                  data={"email": 'acky@test.com', 'password': 'acky'},
                                  follow_redirects=True)

        self.assertNotIn('Welcome back,', result.data)
        self.assertIn('Log In', result.data)
        self.assertIn('Please enter a valid email or password.', result.data)

    def test_process_login_bad_pwd(self):
        """Test to see if the login form will process properly with a known user and wrong password."""

        result = self.client.post("/process-login",
                                  data={"email": 'lucy@test.com', 'password': 'WRONG'},
                                  follow_redirects=True)

        self.assertNotIn('Welcome back,', result.data)
        self.assertIn('Log In', result.data)
        self.assertIn('That email and password combination does not exist.', result.data)

    def test_show_account_not_logged_in(self):
        """Test to see if account page will show up if a user isn't logged in."""

        result = self.client.get("/account")

        self.assertNotIn('Your Account', result.data)
        self.assertIn('/login', result.data)

    # def test_show_account_logged_in(self):  # CURRENTLY NOT WORKING
    #     """Test to see if account page will show up if a user is logged in."""

    #     with app.test_client() as c:
    #         with c.session_transaction() as sess:
    #             sess['user_id'] = '2'

    #     result = self.client.get("/account")

    #     self.assertIn('Your Account', result.data)
    #     self.assertNotIn('/login', result.data)


    #############################################################################
    # Test any functions that will request a JSON response

    # def test_parks_json(self):
    #     response = self.client.get("/parks.json")
    #     # import pdb; pdb.set_trace()
    #     self.assertIsInstance(response, json)

    # def test_visited_parks_json(self):
    #     response = self.client.get("/parks-visited.json")
    #     self.assertEquals(response.json, dict(success=True))


if __name__ == "__main__":
    unittest.main()
