import unittest

import server


class TestCase(unittest.TestCase):
    def test_homepage(self):
        """Tests to see if the index page comes up."""

        test_client = server.app.test_client()
        result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<h1>Parktake <small>Cause the Outdoors Await</small></h1>', result.data)

    def test_signup_page(self):
        """Tests to see if the signup page comes up."""

        test_client = server.app.test_client()
        result = test_client.get('/signup')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<h3>Please register for an account.</h3>', result.data)

    # def test_mark_state_as_visited(self):
    #     park = server.suggest_a_park_for_user(1)
    #     self.assertEqual(park, "Yosemite")

    # def test_incrementing(self):
    #     increment = server.increment_to_dictionary()

    # def test_favorite_color_form(self):
        #     test_client = server.app.test_client()

        #     result = test_client.post('/fav_color', data={'color': 'blue'})
        #     self.assertIn('I like blue, too', result.data)
    def test_logout(self):
        """Tests to see if logout occurs properly."""

        test_client = server.app.test_client()
        result = test_client.get('/logout')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<li><a id="nav-login" href="/login">Log In</a></li>', result.data)

if __name__ == "__main__":
    unittest.main()
