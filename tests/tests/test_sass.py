from django.test import TestCase


class TestSass(TestCase):
    def test_sass(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
