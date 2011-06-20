import unittest
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

class TestUrls(AsyncHTTPTestCase):
    def get_app(self):
        import main
        return Application(main.urls)

    def test_main(self):
        response = self.fetch("/")
        self.assertEqual(response.code, 200)
        assert 'Hello' in response.body

