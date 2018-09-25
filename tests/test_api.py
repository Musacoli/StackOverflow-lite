import unittest
import pytest
from app.models import Users, Questions, Answers
from app.views import app
from app.database import DatabaseConnection
from flask import jsonify, json
from .test_data_generator import TextGenerator
import psycopg2
import json
import jwt
class TestForModels(unittest.TestCase):
    def setUp(self):
        self.quest = Questions()
        self.ans = Answers()
        self.database = DatabaseConnection()
        self.generate = TextGenerator()
        self.user = self.generate.user()
        self.database.create_new_user(self.user, 'test', 'user', '%s@gmail.com'% self.user, 'testpassword')

    def test_if_question_is_added(self):
        assert isinstance(self.quest.add_questions(self.user, self.generate.question(), "I got it from a forum"),  dict) 

    def test_for_duplicate_questionids(self):
        self.quest.add_questions(self.user, self.generate.question(), "I got it from a forum")
        self.quest.add_questions(self.user, self.generate.question(), "I got it from a forum")
        assert  self.database.get_all_questions()[1] != self.database.get_all_questions()[2]

    def test_if_questions_can_be_viewed(self):
        assert isinstance(self.database.get_all_questions(), dict)

    def test_if_a_question_is_viewed(self):
        assert isinstance(self.quest.view_question(1), list)

    def test_if_a_question_can_be_deleted(self):
        self.quest.add_questions(self.user, self.generate.question(), "I got it from a forum")
        for key in self.database.get_latest_question_entry().keys():
            self.database.delete_a_question(key)
        assert IsADirectoryError(self.database.get_all_questions().get(key), KeyError)

    def test_if_an_answer_is_added(self):
        assert isinstance(self.ans.add_answer(1, self.user, self.generate.answer(), 'This is a True/False scenario'), dict)

    def test_for_updating_an_answer(self):
        original_answer = self.database.get_latest_answer_entry()
        for key in original_answer.keys():
            update = self.ans.update_an_answer(key, self.generate.answer())
        assert original_answer != update

    def test_for_commenting_on_an_answer(self):
        question = self.database.get_latest_answer_entry()
        for key in question.keys():
            comment = self.ans.add_comment_to_answer(self.user, key, self.generate.comment())
        assert isinstance(comment, dict)
        
    def test_for_viewing_question_with_most_answers(self):
        assert isinstance(self.ans.view_question_with_most_answers(), dict)


class TestForEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.quest = Questions()
        self.ans = Answers()
        self.database = DatabaseConnection()
        self.generate = TextGenerator()
        self.user = self.generate.user()
        self.database.create_new_user(self.user, 'test', 'user', '%s@gmail.com'% self.user, 'testpassword')
        login = self.client.post('/auth/login', data=json.dumps({"username":self.user, "password":'testpassword'}), content_type="application/json")
        data = json.loads(login.data)
        self.token = data['token']

    def test_for_hello_route(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    def test_for_user_account_creation(self):
        test_user = self.generate.user()
        res = self.client.post('/signup', data=json.dumps({"username":test_user, "firstname":'test', "surname":'user', "email":'%s@gmail.com'% test_user, "password":'testpassword'}), content_type="application/json")
        self.assertEqual(res.status_code, 201)
    
    def test_if_user_account_being_created_already_exists(self):
        res = self.client.post('/signup', data=json.dumps({"username":self.user, "firstname":'test', "surname":'user', "email":'%s@gmail.com'% self.user, "password":'testpassword'}), content_type="application/json")
        self.assertEqual(res.status_code, 409)

    def test_if_user_password_has_a_limit(self):
        test_user = self.generate.user()
        res = self.client.post('/signup', data=json.dumps({"username":test_user, "firstname":'test', "surname":'user', "email":'%s@gmail.com'% test_user, "password":'ord'}), content_type="application/json")
        self.assertEqual(res.status_code, 406)

    def test_if_user_account_creation_accepts_empty_fields(self):
        res = self.client.post('/signup', data=json.dumps({}), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_if_user_is_able_to_login(self):
        res = self.client.post('/auth/login', data=json.dumps({"username":self.user, "password":'testpassword'}), content_type="application/json")
        self.assertEqual(res.status_code, 200)

    def test_if_user_with_invalid_username_can_login(self):
        res = self.client.post('/auth/login', data=json.dumps({"username":'bdyy3yef7878', "password":'testpassword'}), content_type="application/json")
        self.assertEqual(res.status_code, 404)

    def test_if_user_with_invalid_password_can_login(self):
        res = self.client.post('/auth/login', data=json.dumps({"username":self.user, "password":'tesssword'}), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    """def test_for_adding_questions(self):
        res = self.client.post('/questions', data=json.dumps({"title": self.generate.question, "description":"I got it from a forum"}), headers={'x-access-token' : self.token}, content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_for_viewing_all_questions_users_asked(self):
        res = self.client.get('/auth/user/questions', headers={'x-access-token' : self.token})
        self.assertEqual(res.status_code, 200)

    def test_for_adding_a_blank_question(self):
        res = self.client.post('/questions', data=json.dumps(self.quest.add_questions('', '', "")), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_for_adding_already_existing_question(self):
        res = self.client.post('/questions', data=json.dumps(self.quest.add_questions('musa', 'what icvbfs a boolean', "I got it from a forum")), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_for_adding_a_null_question(self):
        res = self.client.post('/questions', data=json.dumps(None), content_type="application/json")
        self.assertEqual(res.status_code, 400)"""

    def test_for_viewing_all_questions(self):
        res = self.client.get('/questions')
        self.assertEqual(res.status_code, 200)

    def test_if_qid_out_of_range(self):
        res = self.client.get('/questions/100000000000000000')
        self.assertEqual(res.status_code, 404)

    def test_for_viewing_a_question(self):
        res = self.client.get('/questions/6')
        self.assertEqual(res.status_code, 200)

    def test_for_searching_for_question(self):
        res = self.client.post('/questions/search', data=json.dumps({"search":"a"}), content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_for_searching_for_question_that_doesnt_exist(self):
        res = self.client.post('/questions/search', data=json.dumps({"search":"an673"}), content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_for_searching_for_question_with_blank_request(self):
        res = self.client.post('/questions/search', data=json.dumps({"search":""}), content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_for_viewing_most_answered_question(self):
        res = self.client.get('/questions/max')
        self.assertEqual(res.status_code, 200)

    """def test_for_deleting_a_question(self):
        res = self.client.delete('/questions/22')
        self.assertEqual(res.status_code, 202)

    def test_for_selecting_preferred_answer(self):
        res = self.client.put('/questions/1/answers/1')
        self.assertEqual(res.status_code, 201)

    def test_for_adding_answers(self):
        res = self.client.post('/questions/1/answers', data=json.dumps(self.ans.add_answer(1, 'collo', 'explangrgsgzgation of a bolean', 'This is a True/False scenario')), content_type="application/json")
        self.assertEqual(res.status_code, 201)"""

if __name__ == '__main__':
    unittest.main()