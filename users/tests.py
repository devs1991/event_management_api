from django.test import TestCase
from rest_framework.test import APIClient

class UserValidationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_duplicate_username(self):
        self.client.post('/api/users/', {'username': 'testuser', 'email': 'test@example.com', 'password': 'password123', 'role': 'attendee'})
        response = self.client.post('/api/users/', {'username': 'testuser', 'email': 'test2@example.com', 'password': 'password123', 'role': 'attendee'})
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        response = self.client.post('/api/users/', {'username': 'testuser', 'email': 'invalidemail', 'password': 'password123', 'role': 'attendee'})
        self.assertEqual(response.status_code, 400)
