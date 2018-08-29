import unittest
import pytest
from app.models import Questions, Answers
from app.views import app
from flask import jsonify, json

class TestForQuestions(unittest.TestCase):
    def setUp(self):
        self.quest = Questions()
        self.ans = Answers()

    def test_if_question_is_added(self):
        assert isinstance(self.quest.add_questions(1, 'what is a boolean', "I got it from a forum"),  dict)

    def test_for_duplicate_questionids(self):
        assert  self.quest.questions[9] == self.quest.questions[10]

    def test_if_questions_can_be_viewed(self):
        assert isinstance(self.quest.view_questions(), dict)

    def test_if_a_question_is_viewed(self):
        assert isinstance(self.quest.view_question(1), dict)

    def test_if_an_answer_is_added(self):
        self.quest.add_questions(1, 'what is a boolean', "I got it from a forum")
        assert isinstance(self.ans.add_answer(2, 'collo', 'explanation of a bolean', 'This is a True/False scenario'), dict)

    def test_if_answers_are_viewed(self):
        self.quest.add_questions(1, 'what is a boolean', "I got it from a forum")
        self.ans.add_answer(2, 'collo', 'explanation of a bolean', 'This is a True/False scenario')
        assert isinstance(self.ans.view_answers(1), dict)

    def test_if_qid_out_of_range(self):
        res = self.quest.view_question(1000)
        assert "Question doesn't exist: Check ID!" == res

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
        res = self.client().post('/questions', data=json.dumps(self.quest.add_questions(1, 'what is a boolean', "I got it from a forum")), content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_for_viewing_all_questions(self):
        self.client().post('/questions', data=json.dumps(self.quest.add_questions(1, 'what is a boolean', "I got it from a forum")), content_type="application/json")
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

    def test_for_viewing_a_question(self):
        self.client().post('/questions', data=json.dumps(self.quest.add_questions(1, 'what is a boolean', "I got it from a forum")), content_type="application/json")
        res = self.client().get('/questions/1')
        self.assertEqual(res.status_code, 200)

    def test_for_viewing_answers(self):
        self.client().post('/questions', data=json.dumps(self.quest.add_questions(1, 'what is a boolean', "I got it from a forum")), content_type="application/json")
        self.client().post('/questions/1/answers', data=json.dumps(self.ans.add_answer(2, 'collo', 'explanation of a bolean', 'This is a True/False scenario')), content_type="application/json")
        res = self.client().get('/questions/1/answers')
        self.assertEqual(res.status_code, 200)

    def test_for_adding_answers(self):
        res = self.client().post('/questions/1/answers', data=json.dumps(self.ans.add_answer(7, 'collo', 'explanation of a bolean', 'This is a True/False scenario')), content_type="application/json")
        self.assertEqual(res.status_code, 201)

if __name__ == '__main__':
    unittest.main()
