import time
from app.database import DatabaseConnection
from passlib.hash import sha256_crypt
import jwt
import datetime


class Users(object):

    def __init__(self):
        self.database = DatabaseConnection()
        self.users = {}
        users = self.database.extract_all_users()
        for user in users:
            self.users[user[0]] = {"firstname": user[1],
                          "surname": user[2],
                          "email": user[3],
                          "password": user[4] }

    def add_user_account(self, user_id, firstname, surname, email, password):
        if user_id not in self.users.keys():
            self.database.create_new_user(user_id, firstname, surname, email, password)
            return "Sign Up Successfull"
        else:
            return "User_ID already exists!"

    def login_user_account(self, user_id, password):
        if user_id in self.users.keys():
            if sha256_crypt.verify(password, self.users[user_id]["password"]):
                return "User: %s has logged in successfully!" % (user_id)
            else:
                return "Password is incorrect, try again"
        else:
            return "Invalid username: Username doesn't exist!"

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm= 'HS256'
            )
        except Exception as e:
            return e
class Questions(Users):

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
        return self.questions[len(self.questions.items())+1]

    def view_questions(self):
        return self.questions

    def view_question(self, qid):
        answers_to_question = {}
        if qid in self.questions.keys():
            ans = self.database.get_answers_to_question(qid)
            for an in ans:
                answers_to_question[an[0]] = {"question_id": an[1],
                                            "user_id": an[2],
                                            "title": an[3],
                                            "description": an[4],
                                            "post_time": an[5]
                                            }
            return self.questions[qid], answers_to_question

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
            return self.answers[len(self.answers.items())]
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
            