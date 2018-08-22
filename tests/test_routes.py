import unittest
import pytest
from app.routes import app

class TestForEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client

    def test_for_hello_route(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    def test_for_viewing_all_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 201)

    def test_for_adding_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 201)

    def test_for_viewing_a_question(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 201)

    def test_for_adding_answers(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 201)

if __name__ == '__main__':
    unittest.main()