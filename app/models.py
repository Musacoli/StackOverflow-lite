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
        return self.database.get_latest_question_entry()

    def view_questions(self):
        return self.database.get_all_questions()

    def view_question(self, qid):
        answers_to_question = self.database.get_answers_to_question(qid)
        text = "ANSWERS TO QUESTION ABOVE"
        return self.questions[qid], text, answers_to_question

    def delete_question(self, qid):
        self.database.delete_a_question(qid)
        return {"message":"Question has been deleted."}

class Answers(Questions):
    def add_answer(self, qid, username, title, description):
        atime = str(time.ctime())
        self.database.create_an_answer(qid, username, title, description, atime)
        return self.database.get_latest_answer_entry()

    def select_preferred_answer(self, aid):
        self.database.select_answer_as_preferred_answer(aid)
        return  {"message":"Operation successful"}
