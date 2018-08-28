import psycopg2

conn = psycopg2.connect(database="stackOL", user="postgres", password="Cm0778404576", host="127.0.0.1", port="5432")
print ("Database has been opened")

cur = conn.cursor()

cur.execute('''CREATE TABLE users
        (user_id TEXT PRIMARY KEY NOT NULL,
        first_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email VARCHAR(20) NOT NULL,
        password TEXT NOT NULL
        );
''')
conn.commit()

cur.execute('''CREATE TABLE questions
        (question_id INT PRIMARY KEY NOT NULL,
        user_id TEXT NOT NULL,
        question_title TEXT NOT NULL,
        description TEXT NOT NULL,
        post_time TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users.user_id
        );
''')

conn.commit()

cur.execute('''CREATE TABLE answers
        (answer_id INT PRIMARY KEY NOT NULL,
        question_id INT NOT NULL,
        user_id TEXT NOT NULL,
        answer_title TEXT ,
        description TEXT NOT NULL,
        post_time TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users.user_id,
        FOREIGN KEY(question_id) REFERENCES questions.question_id
        );
''')
conn.commit()

print ("Tables have been created successfully")

"""cur.execute("INSERT INTO questions (question_id, user_id, question_title, description) \
 VALUES (3, 2, 'What is a boolean2?', 'I found this in a ceratin course')" );
print("Information has been added")"""

"""cur.execute("SELECT * FROM questions")
rows = cur.fetchall()

for row in rows:
    print ("QID= ", row[0])
    print ("UserId= ", row[1])
    print ("Title= ", row[2])
    print ("Descrp.= ", row[3]), "\n"
    
print ("operation successful")"""

"""cur.execute(" UPDATE questions SET question_title = 'How can I append in python?' WHERE question_id = 2 ")
cur.execute("SELECT * FROM questions")
rows = cur.fetchall()

for row in rows:
    print ("QID= ", row[0])
    print ("UserId= ", row[1])
    print ("Title= ", row[2])
    print ("Descrp.= ", row[3]), "\n"
    
print ("operation successful")"""

"""cur.execute("DELETE FROM questions WHERE question_id = 2;")
cur.execute("SELECT * FROM questions")
rows = cur.fetchall()

for row in rows:
    print ("QID= ", row[0])
    print ("UserId= ", row[1])
    print ("Title= ", row[2])
    print ("Descrp.= ", row[3]), "\n"
    
print ("operation successful")"""

conn.commit()
conn.close()