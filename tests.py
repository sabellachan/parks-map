import os
import unittest
from server import app, get_parks
from model import Rec_Area, Visited_Park, db, connect_to_db, example_data_rec_areas, example_data_users, example_data_visits

appkey = os.environ['appkey']
mapkey = os.environ['mapkey']
geocodekey = os.environ['geocodekey']


class ParkTests(unittest.TestCase):
    """Testa for Parktake app for functions that don't require sessions."""

    def setUp(self):
        # set up fake test browser
        self.client = app.test_client()

        # connect to temporary database
        connect_to_db(app, "sqlite:///")

        # This line makes a 500 error in a route raise an error in a test
        app.config['TESTING'] = True

        # create tables and add sample data
        db.create_all()
        example_data_rec_areas()
        example_data_users()
        example_data_visits()

    #############################################################################
    # Test any functions that only render a template.

    def test_load_homepage(self):
        """Tests to see if the index page comes up."""

        result = self.client.get('/')
        # print dir(result) to see what methods are available for result

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<a href="https://ridb.recreation.gov">Recreation Information Database</a>', result.data)

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

        result = self.client.get('/logout')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<a id="nav-login" href="/login">Log In</a>', result.data)

    #############################################################################
    # Test any functions that will query data.

    def test_process_signup_new_user(self):
        """Test to see if the signup form will process new user properly."""

        result = self.client.post('/process-signup',
                                  data={'first_name': "Jane",
                                        'last_name': "Smith",
                                        'zipcode': "94306",
                                        'email': "jane@jane.com",
                                        'password': 'password'},
                                  follow_redirects=True)
        self.assertIn('<a href="/view-park" class="view-parks">View Your Parks</a>', result.data)
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
        self.assertIn('You already have an account. Please login', result.data)

    def test_process_login_known(self):
        """Test to see if the login form will process properly with a known user."""

        result = self.client.post("/process-login",
                                  data={"email": 'lucy@test.com', 'password': 'brindlepuppy'},
                                  follow_redirects=True)

        self.assertIn('Welcome back, Lucy!', result.data)
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

    def test_save_account_not_logged_in(self):
        """Test to see if save account page will show up if a user is not logged in."""

        result = self.client.post('/save-changes', data={'first_name': 'Lucy',
                                                         'last_name': 'Vo',
                                                         'email': 'lucy@test.com',
                                                         'password': 'squirrel',
                                                         'zipcode': '94306'},
                                                   follow_redirects=True)

        self.assertNotIn('Your account has been updated.', result.data)
        self.assertNotIn('Lucy', result.data)
        self.assertIn('/login', result.data)

    #############################################################################
    # Test any functions to see if they're an instance of a built-in class

    def test_get_parks(self):
        """Test to see if this function returns a dictionary."""

        visited_parks = db.session.query(Rec_Area).join(Visited_Park).filter(Visited_Park.user_id == 2).all()

        self.assertIsInstance(get_parks(visited_parks), dict)

class ParkTestsSession(unittest.TestCase):
    """Testa for Parktake app for functions that don't require sessions."""

    def setUp(self):
        # set up fake test browser
        self.client = app.test_client()

        # connect to temporary database
        connect_to_db(app, "sqlite:///")

        # This line makes a 500 error in a route raise an error in a test
        app.config['TESTING'] = True

        # create tables and add sample data
        db.create_all()
        example_data_rec_areas()
        example_data_users()
        example_data_visits()

        # initiate a session
        with self.client as c:
                with c.session_transaction() as sess:
                    sess['user'] = '2'
                c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')

    #############################################################################
    # Test any functions that only render a template.

    def test_load_landing(self):
        """Tests to see if the landing page comes up."""

        result = self.client.get('/landing', data={'mapkey': mapkey}, follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Your Parks', result.data)

    #############################################################################
    # Test any functions that will query data.

    def test_process_login_already_logged(self):
        """Test to see if the login form will show if user is already logged in."""

        result = self.client.get('/login')

        self.assertIn('You are already logged in', result.data)

    def test_show_account_logged_in(self):
        """Test to see if account page will show up if a user is logged in."""

        result = self.client.get('/account')

        self.assertIn('Your Account', result.data)
        self.assertIn('Lucy', result.data)
        self.assertNotIn('/login', result.data)

    def test_update_account_logged_in(self):
        """Test to see if update account page will show up if a user is logged in."""

        result = self.client.get('/update-account')

        self.assertIn('Update Your Account', result.data)
        self.assertIn('Lucy', result.data)
        self.assertNotIn('/login', result.data)

    def test_save_account_logged_in(self):
        """Test to see if save account page will show up if a user is logged in."""

        result = self.client.post('/save-changes', data={'first_name': 'Lucy',
                                                   'last_name': 'Vo',
                                                   'email': 'lucy@test.com',
                                                   'password': 'squirrel',
                                                   'zipcode': '94306'},
                                             follow_redirects=True)

        self.assertIn('Your account has been updated.', result.data)
        self.assertIn('Lucy', result.data)
        self.assertNotIn('/login', result.data)

    def test_view_park(self):
        """Test to see if user can view their parks if a user is logged in."""

        result = self.client.get('/view-park')

        self.assertIn('Based on where you\'ve been,', result.data)

    def test_add_park(self):
        """Test to see if a park will add properly."""

        result = self.client.post('/add-park', data={'park-id': '2941'},
                                               follow_redirects=True)

        self.assertIn('Park Added', result.data)

    #############################################################################
    # Test any functions to see if they're an instance of a built-in class

    def test_parks_json(self):
        """Test to see if /parks.json route will return json object."""

        response = self.client.get("/parks.json")

        self.assertIsInstance(response, object)

    def test_visited_parks_json(self):
        """Test to see if /parks-visited.json route will return json object."""

        response = self.client.get("/parks-visited.json")

        self.assertIsInstance(response, object)

    def test_get_chart_data(self):
        """Test to see if /parks-visited.json route will return json object."""

        response = self.client.get("/parks-in-states.json")

        self.assertIsInstance(response, object)

    #############################################################################
    # Test suggestion feature

    def test_suggestion_feature(self):
        """Test to see if the proper park suggestion is offered."""

        response = self.client.get("/suggest-park")

        self.assertIn('Zion National Park', response.data)


if __name__ == "__main__":
    unittest.main()
