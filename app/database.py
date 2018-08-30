import psycopg2

#Abbreviations of variables
"""
aid = answer_id
qid = question_id
cur = cursor
conn = connection
uid = user_id OR username
"""
class DatabaseConnection(object):

    def __init__(self):
        self.conn = psycopg2.connect(database="stackOLdb", user="postgres", password="Cm0778404576", host="127.0.0.1", port="5432")
        self.cur = self.conn.cursor()
        self.conn.autocommit = True

    def create_users_table(self):
        create_users_table_command = ('''CREATE TABLE users
        (user_id TEXT PRIMARY KEY NOT NULL,
        first_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email VARCHAR(20) NOT NULL UNIQUE,
        password TEXT NOT NULL
        );''')
        self.cur.execute(create_users_table_command)

    def create_new_user(self, user_id, firstname, surname, email, password):
        create_new_user_command = ("INSERT INTO users(user_id, first_name, surname, email, password) VALUES(%s, %s, %s, %s, %s)")
        self.cur.execute(create_new_user_command, (user_id, firstname, surname, email, password))
        #self.conn.commit()
        #self.conn.close()

    def extract_all_users(self):
        self.cur.execute("SELECT * FROM users;")
        users = self.cur.fetchall()
        users_base = {}
        for user in users:
            users_base[user[0]] = {"firstname": user[1],
                            "surname": user[2],
                            "email": user[3],
                            "password": user[4] }
        return users_base

    def create_questions_table(self):
        create_questions_table_command = ('''CREATE TABLE questions
        (question_id SERIAL PRIMARY KEY,
        user_id TEXT NOT NULL,
        question_title TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL,
        post_time TIMESTAMP
        ); ''')
        self.cur.execute(create_questions_table_command)
        #self.conn.commit()
        #self.conn.close()

    def create_a_question(self, user_id, title, description, post_time):
        create_a_question_command = ('''INSERT INTO questions 
        (user_id, question_title, description, post_time)
        VALUES (%s, %s, %s, %s) 
        ''' )
        self.cur.execute(create_a_question_command, (user_id, title, description, post_time))
        #self.conn.commit()
        #self.conn.close()

    def get_all_questions(self):
        self.cur.execute("SELECT * FROM questions;")
        qids = self.cur.fetchall()
        questions_base = {}
        for question in qids:
            questions_base[question[0]] = {"question_title": question[2],
                                    "user_id": question[1],
                                    "description": question[3],
                                    "post_time": question[4]
                                    }
        return questions_base
        #self.conn.close()
    
    def get_latest_question_entry(self):
        self.cur.execute("SELECT * FROM questions ORDER BY question_id DESC;")
        last_question_entry = self.cur.fetchmany(size=1)
        for last_question in last_question_entry:
            return {last_question[0] : {"user_id": last_question[1],
                                "question_title": last_question[2],
                                "description": last_question[3],
                                "post_time": last_question[4]
                            }
                    }

    def get_answers_to_question(self, qid):
        self.cur.execute("SELECT * FROM answers WHERE question_id = %s;", [qid])
        ans = self.cur.fetchall()
        answers_to_question = {}
        for an in ans:
            answers_to_question[an[0]] = {"question_id": an[1],
                                            "user_id": an[2],
                                            "title": an[3],
                                            "description": an[4],
                                            "post_time": an[5]
                                            }
        return answers_to_question

    def delete_a_question(self, qid):
        delete_a_question_command = ("DELETE FROM questions WHERE question_id = %s;")
        self.cur.execute(delete_a_question_command, [qid])
        #self.conn.commit()
        #self.conn.close()

    def create_an_answers_table(self):
        create_an_answers_table_command = ('''CREATE TABLE answers
        (answer_id SERIAL PRIMARY KEY,
        question_id INT NOT NULL,
        user_id TEXT NOT NULL,
        answer_title TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL,
        post_time TIMESTAMP,
        preferred BOOLEAN
        ); ''')
        self.cur.execute(create_an_answers_table_command)
        #self.conn.commit()
        #self.conn.close()

    def create_an_answer(self, question_id, user_id, title, description, post_time):
        create_an_answer_command = ('''INSERT INTO answers 
        (question_id, user_id, answer_title, description, post_time)
        VALUES (%s, %s, %s, %s, %s) 
        ''' )
        self.cur.execute(create_an_answer_command, (question_id, user_id, title, description, post_time))
        #self.conn.commit()
        #self.conn.close()

    def extract_all_answers(self):
        self.cur.execute("SELECT * FROM answers;")
        aids = self.cur.fetchall()
        answers_base = {}
        for answer in aids:
            answers_base[answer[0]] = {"question_id": answer[1],
                                        "user_id": answer[2],
                                        "title": answer[3],
                                        "description": answer[4],
                                        "post_time": answer[5]                                        
                                        }
        return answers_base
        #self.conn.close()

    def get_latest_answer_entry(self):
        self.cur.execute("SELECT * FROM answers ORDER BY answer_id DESC;")
        last_answer_entry = self.cur.fetchmany(size=1)
        for last in last_answer_entry:
            return {last[0] : {"question_id": last[1],
                                "user_id": last[2],
                                "answer_title": last[3],
                                "description": last[4],
                                "post_time": last[5]
                            }
                    }

    def add_new_column_for_selected_answer(self):
        add_column_command = ("ALTER TABLE answers ADD selected BOOLEAN;")
        self.cur.execute(add_column_command)
        #self.conn.commit()
        #self.conn.close()

    def select_answer_as_preferred_answer(self, aid):
        select_answer_command = ("""UPDATE answers SET preferred = True
                                  WHERE answer_id = %s;""")
        self.cur.execute(select_answer_command, [aid])

if __name__ == '__main__':
    database_connection = DatabaseConnection()
    database_connection.conn.close()