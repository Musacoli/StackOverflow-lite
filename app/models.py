import time
from app.database import DatabaseConnection


class Users(object):

    def __init__(self):
        self.users = {}

    def add_user_account(self, username, firstname, surname, email, password):
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.password = password
class Questions(object):

    def __init__(self):
        self.database = DatabaseConnection()
        self.questions = {}
        questions = self.database.extract_all_questions()
        for question in questions:
            self.questions[question[0]] = {"question_title": question[2],
                                            "user_id": question[1],
                                            "description": question[3],
                                            "post_time": question[4]
                                          }
        self.answers = {}
        answers = self.database.extract_all_answers()
        for answer in answers:
            self.answers[answer[0]] = {"question_id": answer[1],
                                        "user_id": answer[2],
                                        "title": answer[3],
                                        "description": answer[4],
                                        "post_time": answer[5]                                        
                                        }

    def add_questions(self, user_id, question_title, description):
        ptime = str(time.ctime())
        self.database.create_a_question(user_id, question_title, description, ptime)
        return self.questions[len(self.questions.items())]

    def view_questions(self):
        return self.questions

    def view_question(self, qid):
        if qid in self.questions.keys():
            return self.questions[qid]
        else:
            return "Question doesn't exist: Check ID!"

    def delete_question(self, qid):
        if qid in self.questions.keys():
            self.database.delete_a_question(qid)
            return "Question has been deleted."
        else:
            return "Unable to delete question which doesn't exist: Check ID!"

class Answers(Questions):
    def add_answer(self, qid, user_id, title, description):
        atime = str(time.ctime())
        if qid in self.questions.keys():
            self.database.create_an_answer(qid, user_id, title, description, atime)
            return self.answers[qid]
        else:
            return "Question doesn't exist: Check ID!"

    def view_answers(self, aid):
            return self.answers[aid]

    def select_preferred_answer(self, aid):
        if aid in self.answers.keys():
            self.database.select_answer_as_preferred_answer(aid)
            return "Operation successful"
        else:
            "Question doesn't exist: Check ID!"
            