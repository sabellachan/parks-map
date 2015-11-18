import unittest

import server


class TestPageLoads(unittest.TestCase):
    """Test any functions that simply render a template."""

    def setUp(self):
        self.client = server.app.test_client()

    def test_load_homepage(self):
        """Tests to see if the index page comes up."""

        result = self.client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<h1>Parktake <small>Cause the Outdoors Await</small></h1>', result.data)

    def test_load_signup(self):
        """Tests to see if the signup page comes up."""

        result = self.client.get('/signup')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<h3>Please register for an account.</h3>', result.data)

    def test_load_login(self):
        """Tests to see if the signup page comes up."""

        result = self.client.get('/login')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<h3>Please register for an account.</h3>', result.data)  ####

    def test_load_logout(self):
        """Tests to see if logout occurs properly."""

        test_client = server.app.test_client()
        result = test_client.get('/logout')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<a id="nav-login" href="/login">Log In</a>', result.data)


class TestQueryData(unittest.TestCase):
    """Test any functions that will query data from the database."""

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

    def test_process_login(self):
        """Tests to see if the login form will process properly with a known user."""

        result = self.client.post('/process-login',
                                  data={'email': 'test@test.com',
                                        'password': 'n'},
                                  follow_redirects=True)
        self.assertIn('<p>Welcome back,', result.data)
        self.assertNotIn('<a id="nav-login" href="/login">Log In</a>', result.data)


    # def test_mark_state_as_visited(self):
    #     park = server.suggest_a_park_for_user(1)
    #     self.assertEqual(park, "Yosemite")

    # def test_incrementing(self):
    #     increment = server.increment_to_dictionary()

    # def test_favorite_color_form(self):
        #     test_client = server.app.test_client()

        #     result = test_client.post('/fav_color', data={'color': 'blue'})
        #     self.assertIn('I like blue, too', result.data)

if __name__ == "__main__":
    unittest.main()
