import psycopg2


class DatabaseConnection(object):

    def __init__(self):
        self.conn = psycopg2.connect(database="stackOL", user="postgres", password="Cm0778404576", host="127.0.0.1", port="5432")
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

    def create_new_user(self, username, firstname, surname, email, password):
        create_new_user_command = ('''INSERT INTO users 
        (user_id, first_name, surname, email, password)
        VALUES (%s, %s, %s, %s, %s) 
        ''' % (username, firstname, surname, email, password))
        self.cur.execute(create_new_user_command)

    def create_questions_table(self):
        create_questions_table_command = ('''CREATE TABLE questions
        (question_id INT PRIMARY KEY NOT NULL,
        user_id TEXT NOT NULL,
        question_title TEXT NOT NULL,
        description TEXT NOT NULL,
        post_time TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users.user_id
        ); ''')
        self.cur.execute(create_questions_table_command)

    def create_a_question(self, question_id, user_id, title, description, post_time):
        create_a_question_command = ('''INSERT INTO questions 
        (question_id, user_id, question_title, description, post_time)
        VALUES (%s, %s, %s, %s, %s) 
        ''' % (question_id, user_id, title, description, post_time))
        self.cur.execute(create_a_question_command)

    def create_an_answers_table(self):
        create_an_answers_table_command = ('''CREATE TABLE answers
        (answer_id INT PRIMARY KEY NOT NULL,
        question_id INT NOT NULL,
        user_id TEXT NOT NULL,
        answer_title TEXT ,
        description TEXT NOT NULL,
        post_time TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users.user_id,
        FOREIGN KEY(question_id) REFERENCES questions.question_id
        ); ''')
        self.cur.execute(create_an_answers_table_command)

    def create_an_answer(self, answer_id, question_id, user_id, title, description, post_time):
        create_an_answer_command = ('''INSERT INTO answers 
        (answer_id, question_id, user_id, answer_title, description, post_time)
        VALUES (%s, %s, %s, %s, %s) 
        ''' % (answer_id, question_id, user_id, title, description, post_time))
        self.cur.execute(create_an_answer_command)

