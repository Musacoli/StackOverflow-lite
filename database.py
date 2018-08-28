import psycopg2

conn = psycopg2.connect(database="stackdb", user="postgres", password="Cm0778404576", host="127.0.0.1", port="5432")
print ("Database has been opened")

cur = conn.cursor()

"""cur.execute('''CREATE TABLE questions
        (question_id INT PRIMARY KEY NOT NULL,
        user_id INT NOT NULL,
        question_title TEXT NOT NULL,
        description TEXT NOT NULL
        );
''')
"""
"""cur.execute("INSERT INTO questions (question_id, user_id, question_title, description) \
 VALUES (3, 2, 'What is a boolean2?', 'I found this in a ceratin course')" );
print("Information has been added")"""

cur.execute("")

conn.commit()
conn.close()