import unittest
import pytest
from app.models import Users, Questions, Answers
from app.views import app
from flask import jsonify, json

class TestForQuestions(unittest.TestCase):
    def setUp(self):
        self.quest = Questions()
        self.ans = Answers()

    def test_if_question_is_added(self):
        assert isinstance(self.quest.add_questions('musa', 'what is a hexadecimal', "I got it from a forum"),  dict)

    def test_for_duplicate_questionids(self):
        assert  self.quest.questions[1] != self.quest.questions[5]

    def test_if_questions_can_be_viewed(self):
        assert isinstance(self.quest.view_questions(), dict)

    def test_if_a_question_is_viewed(self):
        assert isinstance(self.quest.view_question(1), tuple)

    def test_if_an_answer_is_added(self):
        assert isinstance(self.ans.add_answer(1, 'collo', 'explanation of a tuple', 'This is a True/False scenario'), dict)


class TestForEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.quest = Questions()
        self.ans = Answers()

    def test_for_hello_route(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    def test_for_adding_questions(self):
        res = self.client().post('/questions', data=json.dumps(self.quest.add_questions('musa', 'what is a boolean', "I got it from a forum")), content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_for_viewing_all_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

    def test_if_qid_out_of_range(self):
        res = self.client().get('/questions/1000')
        self.assertEqual(res.status_code, 400)

    def test_for_viewing_a_question(self):
        res = self.client().get('/questions/1')
        self.assertEqual(res.status_code, 200)

    def test_for_adding_answers(self):
        res = self.client().post('/questions/1/answers', data=json.dumps(self.ans.add_answer(1, 'collo', 'explanation of a bolean', 'This is a True/False scenario')), content_type="application/json")
        self.assertEqual(res.status_code, 201)

if __name__ == '__main__':
    unittest.main()
