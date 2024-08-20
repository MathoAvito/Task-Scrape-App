import unittest
from website import create_app

class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test client for the Flask app."""
        cls.app = create_app()
        cls.app.testing = True
        cls.client = cls.app.test_client()

    def test_home_page(self):
        """Test the login page route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Adjust 'Welcome' based on your actual content

    def test_about_page(self):
        """Test the sign-up page route."""
        response = self.client.get('/sign-up')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign-Up', response.data)  # Adjust 'About' based on your actual content

    def test_non_existent_page(self):
        """Test a non-existent page."""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

#     def test_post_route(self):
#         """Test a POST route."""
#         response = self.client.post('/submit', data=dict(name='test'))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Success', response.data)  # Adjust 'Success' based on your actual content

if __name__ == "__main__":
    unittest.main()
