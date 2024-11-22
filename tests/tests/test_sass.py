import os.path
from django.conf import settings
from django.test import TestCase

from django_libsass import compile

class TestSass(TestCase):
    def test_invocation(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_import(self):
        result = compile(filename=os.path.join(settings.BASE_DIR, 'tests', 'static', 'css', 'with_import.scss'))
        self.assertIn('.imported-style', result)

    def test_extra_include_path(self):
        result = compile(filename=os.path.join(settings.BASE_DIR, 'tests', 'static', 'css', 'with_extra_include.scss'))
        self.assertIn('.extra-style', result)

    def test_raw_css_import(self):
        result = compile(filename=os.path.join(settings.BASE_DIR, 'tests', 'static', 'css', 'with_raw_css_import.scss'))
        self.assertIn('.raw-style-1', result)
        self.assertIn('.raw-style-2', result)

    def test_static_function(self):
        result = compile(filename=os.path.join(settings.BASE_DIR, 'tests', 'static', 'css', 'with_static.scss'))
        self.assertIn(r'background-image: url(/static/images/my%20image.jpg);', result)
