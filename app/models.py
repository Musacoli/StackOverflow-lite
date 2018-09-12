import time
from app.database import DatabaseConnection
from passlib.hash import sha256_crypt
import jwt
import datetime


class Users(object):

    def __init__(self):
        self.database = DatabaseConnection()
        self.users = self.database.extract_all_users()

    def add_user_account(self, username, firstname, surname, email, password):
        self.database.create_new_user(username, firstname, surname, email, password)
        return {"message":"Sign Up Successfull"}

class Questions(Users):

    def __init__(self):
        self.database = DatabaseConnection()
        self.questions = self.database.get_all_questions()
        self.answers = self.database.extract_all_answers()

    def add_questions(self, username, question_title, description):
        ptime = str(time.ctime())
        self.database.create_a_question(username, question_title, description, ptime)
        return self.database.get_all_questions()[len(self.database.get_all_questions().keys())]

    def view_question(self, qid):
        answers_to_question = self.database.get_answers_to_question(qid)
        text = "ANSWERS TO QUESTION ABOVE"
        return self.database.get_all_questions()[qid], text, answers_to_question

    def delete_question(self, qid):
        self.database.delete_a_question(qid)
        return {"message":"Question has been deleted."}

class Answers(Questions):
    def add_answer(self, qid, username, title, description):
        atime = str(time.ctime())
        self.database.create_an_answer(qid, username, title, description, atime)
        return self.database.extract_all_answers()[len(self.database.extract_all_answers().keys())]

    def update_an_answer(self, answer_id, new_answer):
        self.database.update_an_existing_answer(answer_id, new_answer)
        return self.database.extract_all_answers()[answer_id]

    def select_preferred_answer(self, aid):
        self.database.select_answer_as_preferred_answer(aid)
        return  {"message":"Operation successful"}

    def add_comment_to_answer(self, username, answer_id, comment):
        post_time = str(time.ctime())
        self.database.add_comment_to_answer(username, answer_id, comment, post_time)
        return self.database.extract_all_comments()

    def view_question_with_most_answers(self):
        qid = self.database.view_question_with_most_answers()
        return self.database.get_all_questions()[qid]