from flask import Flask

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

    def test_mark_state_as_visited(self):
        park = server.suggest_a_park_for_user(1)
        self.assertEqual(park, "Yosemite")

    # def test_favorite_color_form(self):
    #     test_client = server.app.test_client()

    #     result = test_client.post('/fav_color', data={'color': 'blue'})
    #     self.assertIn('I like blue, too', result.data)

if __name__ == "__main__":
    unittest.main()
