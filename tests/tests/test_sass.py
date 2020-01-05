from django.test import TestCase


print("hello from test_sass")

class TestSass(TestCase):
    def test_sass(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
