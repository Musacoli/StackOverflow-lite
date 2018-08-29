import psycopg2

#Abbreviations of variables
"""
aid = answer_id
qid = question_id
cur = cursor
conn = connection
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
        email VARCHAR(20) NOT NULL,
        password TEXT NOT NULL
        );''')
        self.cur.execute(create_users_table_command)

    def create_new_user(self, user_id, firstname, surname, email, password):
        create_new_user_command = ("INSERT INTO users(user_id, first_name, surname, email, password) VALUES(%s, %s, %s, %s, %s)")
        self.cur.execute(create_new_user_command, (user_id, firstname, surname, email, password))
        #self.conn.commit()
        #self.conn.close()

    def create_questions_table(self):
        create_questions_table_command = ('''CREATE TABLE questions
        (question_id SERIAL PRIMARY KEY,
        user_id TEXT NOT NULL,
        question_title TEXT NOT NULL,
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

    def extract_all_questions(self):
        self.cur.execute("SELECT * FROM questions;")
        qids = self.cur.fetchall()
        return qids
        #self.conn.close()

    def delete_a_question(self, qid):
        delete_a_question_command = ("DELETE FROM questions WHERE question_id = %s;")
        self.cur.execute(delete_a_question_command, qid)
        #self.conn.commit()
        #self.conn.close()

    def create_an_answers_table(self):
        create_an_answers_table_command = ('''CREATE TABLE answers
        (answer_id SERIAL PRIMARY KEY,
        question_id INT NOT NULL,
        user_id TEXT NOT NULL,
        answer_title TEXT ,
        description TEXT NOT NULL,
        post_time TIMESTAMP
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
        return aids
        #self.conn.close()

    def add_new_column_for_selected_answer(self):
        add_column_command = ("ALTER TABLE answers ADD selected BOOLEAN;")
        self.cur.execute(add_column_command)
        #self.conn.commit()
        #self.conn.close()

    def select_answer_as_preferred_answer(self, aid):
        select_answer_command = ("""INSERT INTO answers (selected)
                                 VALUES(1) WHERE answer_id=%s;""")
        self.cur.execute(select_answer_command, (aid))

if __name__ == '__main__':
    database_connection = DatabaseConnection()