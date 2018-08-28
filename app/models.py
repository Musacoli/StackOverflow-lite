import time
from app.database import DatabaseConnection


class Users(object):

    def __init__(self, username, firstname, surname, email, password):
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.password = password
class Questions(object):

    def __init__(self):
        self.database = DatabaseConnection()
        self.questions = {}
        self.answers = {}

    def add_questions(self, user_id, title, description):
        ptime = str(time.ctime())
        self.database.create_a_question(user_id, title, description, ptime)

    
    def view_questions(self):
        questions = self.database.extract_all_questions()
        for question in questions:
            self.questions[question[0]] = {"question_title": question[2],
                                                "user_id": question[1],
                                                "description": question[3],
                                                "post_time": question[4]
                                                }
        return self.questions

    def view_question(self, qid):
        if qid in self.questions.keys():
            return self.questions[qid]
        else:
            return 'Question not found'

class Answers(Questions):
    def add_answer(self, qid, answer):
        atime = str(time.ctime())
        self.answers[qid] = {"answer" : answer,
                            "time" : atime 
                            }
        return self.answers[qid]

    def view_answers(self, qid):
            return self.answers[qid]

test = Questions()
print (test.view_questions())