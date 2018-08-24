import unittest
import pytest
from app.models import Questions, Answers
from app.views import app
from flask import jsonify

class TestForQuestions(unittest.TestCase):
    def setUp(self):
        self.quest = Questions()
        self.ans = Answers()

    def test_if_question_is_added(self):
        assert isinstance(self.quest.add_questions('What is a boolean'),  dict)

    def test_if_questions_can_be_viewed(self):
        assert isinstance(self.quest.view_questions(), dict)

    def test_if_a_question_is_viewed(self):
        self.quest.add_questions('What is a boolean')
        assert isinstance(self.quest.view_question(1), dict)

    def test_if_an_answer_is_added(self):
        self.quest.add_questions('What is a boolean')
        assert isinstance(self.ans.add_answer(1,'the answer'), dict)

    def test_if_answers_are_viewed(self):
        self.quest.add_questions('What is a boolean')
        self.ans.add_answer(1,'the answer')
        assert isinstance(self.ans.view_answers(1), dict)

class TestForEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.quest = Questions()
        self.ans = Answers()

    def test_for_hello_route(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    def test_for_viewing_all_questions(self):
        self.client().post('/questions', data=jsonify(self.quest.add_questions("What is a boolean?")))
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 201)

    """def test_for_adding_questions(self):
        res = self.client().post('/questions')
        self.assertEqual(res.status_code, 201)

    def test_for_viewing_a_question(self):
        res = self.client().get('/questions/<int:questionid>')
        self.assertEqual(res.status_code, 201)

    def test_for_viewing_answers(self):
        res = self.client().get('/questions/<int:questionid>/answers')
        self.assertEqual(res.status_code, 201)

    def test_for_adding_answers(self):
        res = self.client().post('/questions<int:questionid>/answers')
        self.assertEqual(res.status_code, 201)"""

if __name__ == '__main__':
    unittest.main()
