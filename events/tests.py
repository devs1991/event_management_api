from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User

class EventValidationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.organizer = User.objects.create_user(username='organizer', email='organizer@example.com', role='event_organizer', password='password123')

    def test_past_event_date(self):
        self.client.login(username='organizer', password='password123')
        response = self.client.post('/api/events/', {
            'title': 'Past Event',
            'location': 'Test Location',
            'date': '2023-01-01',
            'time': '18:00:00',
            'max_attendees': 10,
            'organizer': self.organizer.id,
        })
        self.assertEqual(response.status_code, 400)

    def test_negative_max_attendees(self):
        response = self.client.post('/api/events/', {
            'title': 'Negative Attendees',
            'location': 'Test Location',
            'date': '2024-12-31',
            'time': '18:00:00',
            'max_attendees': -5,
            'organizer': self.organizer.id,
        })
        self.assertEqual(response.status_code, 400)
