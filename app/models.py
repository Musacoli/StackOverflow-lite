import time
from app.database import DatabaseConnection
import datetime


class Users(object):

    def __init__(self):
        self.database = DatabaseConnection()
        self.users = self.database.extract_all_users()

class Questions(Users):

    def __init__(self):
        self.database = DatabaseConnection()
        self.questions = self.database.get_all_questions()
        self.answers = self.database.extract_all_answers()

    def add_questions(self, username, question_title, description):
        ptime = str(time.ctime())
        self.database.create_a_question(username, question_title, description, ptime)
        return self.database.get_latest_question_entry()

    def view_question(self, qid):
        answers_to_question = self.database.get_answers_to_question(qid)
        text = "ANSWERS TO QUESTION ABOVE"
        return [self.database.get_all_questions()[qid], text, answers_to_question]

class Answers(Questions):
    def add_answer(self, qid, username, title, description):
        atime = str(time.ctime())
        self.database.create_an_answer(qid, username, title, description, atime)
        return self.database.get_latest_answer_entry()

    def update_an_answer(self, answer_id, new_answer):
        self.database.update_an_existing_answer(answer_id, new_answer)
        return self.database.extract_all_answers()[answer_id]

    def add_comment_to_answer(self, username, answer_id, comment):
        post_time = str(time.ctime())
        self.database.add_comment_to_answer(username, answer_id, comment, post_time)
        return self.database.extract_all_comments()

    def view_question_with_most_answers(self):
        qid = self.database.view_question_with_most_answers()
        return self.database.get_all_questions()[qid]