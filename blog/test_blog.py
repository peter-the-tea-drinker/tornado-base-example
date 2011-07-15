import unittest
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
import blog
blog.make_fixtures()

class TestBlog(AsyncHTTPTestCase):
    def get_app(self):
        return Application(blog.urls)

    def test_index(self):
        response = self.fetch("/")
        self.assertEqual(response.code, 200)
        assert 'Blog Index' in response.body

    def test_impo(self):
        import main
