import unittest
import pytest
from app.models import Users, Questions, Answers
from app.views import app
from app.database import DatabaseConnection
from flask import jsonify, json
from .test_data_generator import TextGenerator
import psycopg2

class TestForModels(unittest.TestCase):
    def setUp(self):
        self.quest = Questions()
        self.ans = Answers()
        self.user = Users()
        self.database = DatabaseConnection()
        self.generate = TextGenerator()

    def test_if_question_is_added(self):
        user = self.generate.user()
        self.database.create_new_user(user, 'test', 'user', '%s@gmail.com'% user, 'testpassword')
        assert isinstance(self.quest.add_questions(user, self.generate.question(), "I got it from a forum"),  dict) 

    def test_for_duplicate_questionids(self):
        user = self.generate.user()
        self.database.create_new_user(user, 'test', 'user','%s@gmail.com'% user, 'testpassword')
        self.quest.add_questions(user, self.generate.question(), "I got it from a forum")
        self.quest.add_questions(user, self.generate.question(), "I got it from a forum")
        assert  self.database.get_all_questions()[1] != self.database.get_all_questions()[2]

    def test_if_questions_can_be_viewed(self):
        assert isinstance(self.database.get_all_questions(), dict)

    def test_if_a_question_is_viewed(self):
        assert isinstance(self.quest.view_question(1), list)

    """def test_if_a_question_can_be_deleted(self):
        user = self.generate.user()
        self.database.create_new_user(user, 'test', 'user', '%s@gmail.com'% user, 'testpassword')
        self.database.delete_a_question(self.database.get_latest_question_entry().keys)
        assert isinstance(self.quest.view_question(8), KeyError)"""

    def test_if_an_answer_is_added(self):
        user = self.generate.user()
        self.database.create_new_user(user, 'test', 'user','%s@gmail.com'% user, 'testpassword')
        assert isinstance(self.ans.add_answer(1, user, self.generate.answer(), 'This is a True/False scenario'), dict)


"""class TestForEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.quest = Questions()
        self.ans = Answers()
        self.user = Users()

    def test_for_hello_route(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    def test_for_user_account_creation(self):
        res = self.client().post('/signup', data=json.dumps(self.user.add_user_account('mako', 'mark', 'munanura', 'markmun@gmail.com', 'password')), content_type="application/json")
        self.assertEqual(res.status_code, 201)
    
    def test_if_user_account_being_created_already_exists(self):
        res = self.client().post('/signup', data=json.dumps(self.user.add_user_account('mako', 'mark', 'munanura', 'markmun@gmail.com', 'password')), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_if_user_account_creation_accepts_empty_fields(self):
        res = self.client().post('/signup', data=json.dumps(self.user.add_user_account('', '', '', '', '')), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_if_user_is_able_to_login(self):
        res = self.client().post('/auth/login', data=json.dumps(('mako', 'password')), content_type="application/json")
        self.assertEqual(res.status_code, 200)

    def test_if_user_with_invalid_username_can_login(self):
        res = self.client().post('/auth/login', data=json.dumps(('makchsj', 'password')), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_if_user_with_invalid_password_can_login(self):
        res = self.client().post('/auth/login', data=json.dumps(('mako', 'passwordaer')), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_for_adding_questions(self):
        res = self.client().post('/questions', data=json.dumps(self.quest.add_questions('musa', 'what icvbfs a boolean', "I got it from a forum")), content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_for_adding_a_blank_question(self):
        res = self.client().post('/questions', data=json.dumps(self.quest.add_questions('', '', "")), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_for_adding_already_existing_question(self):
        res = self.client().post('/questions', data=json.dumps(self.quest.add_questions('musa', 'what icvbfs a boolean', "I got it from a forum")), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_for_adding_a_null_question(self):
        res = self.client().post('/questions', data=json.dumps(None), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_for_viewing_all_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

    def test_for_viewing_questions_when_database_is_empty(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 404)

    def test_if_qid_out_of_range(self):
        res = self.client().get('/questions/1000')
        self.assertEqual(res.status_code, 400)

    def test_for_viewing_a_question(self):
        res = self.client().get('/questions/6')
        self.assertEqual(res.status_code, 200)

    def test_for_deleting_a_question(self):
        res = self.client().delete('/questions/22')
        self.assertEqual(res.status_code, 202)

    def test_for_selecting_preferred_answer(self):
        res = self.client().put('/questions/1/answers/1')
        self.assertEqual(res.status_code, 201)

    def test_for_adding_answers(self):
        res = self.client().post('/questions/1/answers', data=json.dumps(self.ans.add_answer(1, 'collo', 'explangrgsgzgation of a bolean', 'This is a True/False scenario')), content_type="application/json")
        self.assertEqual(res.status_code, 201)"""

if __name__ == '__main__':
    unittest.main()
