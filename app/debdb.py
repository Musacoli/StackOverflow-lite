#from database import DatabaseConnection

#database = DatabaseConnection()
#database.create_users_table()
#database.create_questions_table()
#database.create_an_answers_table()
#database.create_new_user('nelo', 'nelson', 'mwiru', 'nmwiru@gmail.com','mukenene')
#database.create_questions_table()
#database.create_a_question(1, 'what is a boolean', "I got it from a forum", 'Tue 20 August 2018')
#database.create_an_answer(2, 'collo', 'explanation of a bolean', 'This is a True/False scenario', 'Wed 29 August 2018')
#database.add_new_column_for_selected_answer()
"""cur.execute('''CREATE TABLE users
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

print ("Tables have been created successfully")"""

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

"""@app.route('/questions/<int:questionid>/answers', methods=['POST'])
def add_an_answer(questionid):
elif answer.isdigit():
            return make_response(jsonify("Invalid Input, please try again!")), 400
        elif (answer == None) or (len(answer) <= 0) or answer.isspace():
            return make_response(jsonify("REQUIRED FIELD: Don't leave blank or submit spaces!")), 400"""