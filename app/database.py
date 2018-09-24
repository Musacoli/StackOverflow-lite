import psycopg2
from passlib.hash import sha256_crypt

#Abbreviations of variables
"""
aid = answer_id
qid = question_id
cur = cursor
conn = connection
uid = username       """
class DatabaseConnection(object):
          
    def create_users_table(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        create_users_table_command = ('''CREATE TABLE IF NOT EXISTS users
        (userid SERIAL,
        username TEXT NOT NULL,
        first_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email VARCHAR(20) NOT NULL UNIQUE,
        password TEXT NOT NULL,
        PRIMARY KEY (username)
        );''')
        self.cur.execute(create_users_table_command)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def create_new_user(self, username, firstname, surname, email, pasword):
        password = sha256_crypt.encrypt(pasword)
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        create_new_user_command = ("INSERT INTO users(username, first_name, surname, email, password) VALUES(%s, %s, %s, %s, %s)")
        self.cur.execute(create_new_user_command, (username, firstname, surname, email, password))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def extract_all_users(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM users;")
        users = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        users_base = {}
        for user in users:
            users_base[user[1]] = {"firstname": user[2],
                            "surname": user[3],
                            "email": user[4],
                            "password": user[5] }
        return users_base
    

    def create_questions_table(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        create_questions_table_command = ('''CREATE TABLE IF NOT EXISTS questions
        (question_id SERIAL,
        username TEXT NOT NULL,
        question_title TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL,
        post_time TIMESTAMP,
        PRIMARY KEY (question_id),
        FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
        ); ''')
        self.cur.execute(create_questions_table_command)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def create_a_question(self, username, title, description, post_time):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        create_a_question_command = (' INSERT INTO questions (username, question_title, description, post_time) VALUES (%s, %s, %s, %s) ' )
        self.cur.execute(create_a_question_command, (username, title, description, post_time))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_all_questions(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM questions;")
        qids = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        questions_base = {}
        for question in qids:
            questions_base[question[0]] = {"question_title": question[2],
                                    "username": question[1],
                                    "description": question[3],
                                    "post_time": question[4]
                                    }
        return questions_base
    
    def get_latest_question_entry(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM questions ORDER BY question_id DESC LIMIT 1;")
        last_question_entry = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        for last_question in last_question_entry:
            return {last_question[0] : {"username": last_question[1],
                                "question_title": last_question[2],
                                "description": last_question[3],
                                "post_time": last_question[4]
                            }
                    }
    def get_question(self, question_id):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM questions WHERE question_id = {}").format(question_id)
        question = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        for quest in question:
            return {quest[0] : {"username": quest[1],
                                "question_title": quest[2],
                                "description": quest[3],
                                "post_time": quest[4]}
                    }

    def get_all_users_questions(self, username):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM questions WHERE username = %s;", [username])
        user_questions = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        questions = {}
        for quest in user_questions:
            questions[quest[0]] = {"username": quest[1],
                                    "title": quest[2],
                                    "description": quest[3],
                                    "post_time": quest[4]
                                }
        return questions


    def get_answers_to_question(self, qid):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM answers WHERE question_id = %s;", [qid])
        ans = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        answers_to_question = {}
        for an in ans:
            answers_to_question[an[0]] = {"question_id": an[1],
                                            "username": an[2],
                                            "title": an[3],
                                            "description": an[4],
                                            "post_time": an[5]
                                            }
        return answers_to_question

    def delete_a_question(self, qid):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        delete_a_question_command = ("DELETE FROM questions WHERE question_id = %s;")
        self.cur.execute(delete_a_question_command, [qid])
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def search_for_question(self, search_phrase):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        search_command = ("SELECT * FROM questions WHERE question_title ILIKE %s ; ")
        pattern = '%{}%'.format(search_phrase)
        self.cur.execute(search_command, (pattern,))
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        questions = {}
        for quest in result:
            questions[quest[0]] = {"username": quest[1],
                                    "title": quest[2],
                                    "description": quest[3],
                                    "post_time": quest[4]
                                }
        return questions


    def view_question_with_most_answers(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        view_command = ('SELECT question_id, COUNT(answer_title) AS "answer" FROM answers GROUP BY question_id ORDER BY 2 LIMIT 1; ')
        self.cur.execute(view_command)
        question = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        for quest in question:
            return quest[0]
    
    def create_an_answers_table(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        create_an_answers_table_command = ('''CREATE TABLE IF NOT EXISTS answers
        (answer_id SERIAL,
        question_id INT NOT NULL,
        username TEXT NOT NULL,
        answer_title TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL,
        post_time TIMESTAMP,
        preferred BOOLEAN,
        upvotes INT DEFAULT 0,
        downvotes INT DEFAULT 0,
        PRIMARY KEY (answer_id),
        FOREIGN KEY (question_id) REFERENCES questions (question_id) ON DELETE CASCADE,
        FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
        ); ''')
        self.cur.execute(create_an_answers_table_command)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def create_an_answer(self, question_id, username, title, description, post_time):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        create_an_answer_command = (' INSERT INTO answers (question_id, username, answer_title, description, post_time) VALUES (%s, %s, %s, %s, %s) ')
        self.cur.execute(create_an_answer_command, (question_id, username, title, description, post_time))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def extract_all_answers(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM answers;")
        aids = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        answers_base = {}
        for answer in aids:
            answers_base[answer[0]] = {"question_id": answer[1],
                                        "username": answer[2],
                                        "title": answer[3],
                                        "description": answer[4],
                                        "post_time": answer[5]                                        
                                        }
        return answers_base

    def get_latest_answer_entry(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM answers ORDER BY answer_id DESC LIMIT 1;")
        last_answer_entry = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        for last in last_answer_entry:
            return {last[0] : {"question_id": last[1],
                                "username": last[2],
                                "answer_title": last[3],
                                "description": last[4],
                                "post_time": last[5]
                            }
                    }

    def update_an_existing_answer(self, answer_id, new_answer):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        update_answer_command = ('UPDATE answers SET description = %s WHERE answer_id = %s;')
        self.cur.execute(update_answer_command, (new_answer,answer_id))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def select_answer_as_preferred_answer(self, aid):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        select_answer_command = ("""UPDATE answers SET preferred = True
                                WHERE answer_id = %s;""")
        self.cur.execute(select_answer_command, [aid])
        self.conn.commit()
        self.cur.close()
        self.conn.close()
    
    def upvote_answer(self, answer_id):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute('UPDATE answers SET upvotes =upvotes +1 WHERE answer_id = %s; '% (answer_id))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def downvote_answer(self, answer_id):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute('UPDATE answers SET downvotes = downvotes +1 WHERE answer_id = %s; '% (answer_id))
        self.conn.commit()
        self.cur.close()
        self.conn.close()
    
    def create_comments_table(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        create_questions_table_command = ('''CREATE TABLE IF NOT EXISTS comments
        (comment_id SERIAL,
        username TEXT NOT NULL,
        answer_id INT NOT NULL,
        comment TEXT NOT NULL UNIQUE,
        post_time TIMESTAMP,
        PRIMARY KEY (comment_id),
        FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE,
        FOREIGN KEY (answer_id) REFERENCES answers (answer_id) ON DELETE CASCADE
        ); ''')
        self.cur.execute(create_questions_table_command)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def add_comment_to_answer(self, username, answer_id, comment, post_time):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        add_comment_command= ('INSERT INTO comments (username, answer_id, comment, post_time) VALUES (%s,%s,%s,%s);')
        self.cur.execute(add_comment_command, (username, answer_id, comment, post_time))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def extract_all_comments(self):
        self.conn = psycopg2.connect(database="dcfkj3ivcuaqbu", user="qzbfyxixkixkft", password="d8b4ba70fe124cb34085745edcff405a056451ff635978eee11efa337bd36aa2", host="ec2-54-221-237-246.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT * FROM comments ORDER BY comment_id DESC LIMIT 1;')
        comment = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        for com in comment:
            return {com[0] : {"username": com[1],
                                "answer_id": com[2],
                                "comment": com[3],
                                "post_time": com[4]
                                }
                    }

    """except:

            def create_database(self):
                self.conn = psycopg2.connect(database="postgres", user="postgres", password="Cm0778404576", host="127.0.0.1", port="5432")
                self.cur = self.conn.cursor()
                self.cur.execute("CREATE DATABASE stackOLdb;")
                self.cur.close()
                self.conn.close()
            continue"""

create = DatabaseConnection()
create.create_users_table()
create.create_questions_table()
create.create_an_answers_table()
create.create_comments_table()

if __name__ == '__main__':
    database_connection = DatabaseConnection()
