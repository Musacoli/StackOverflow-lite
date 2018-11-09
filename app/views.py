from flask import Flask, request, jsonify, abort, make_response
from app.models import Users, Questions, Answers
from app.database import DatabaseConnection
from passlib.hash import sha256_crypt
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config["SECRET_KEY"] = 'thisisstackoverflowlite'

user = Users()
stack = Questions()
ans = Answers()
database = DatabaseConnection()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response(jsonify({'message': 'Token is missing'})), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = data['username']
        except:
            return make_response(jsonify({'message': 'Token is invalid'})), 403

        return f(current_user, *args, **kwargs)
    return decorated

@app.errorhandler(400)
def page_not_found(e):
    return make_response(jsonify({"status":-1, "message":"Invalid Input/Bad Request, please try again!"})), 400

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return jsonify('Welcome to the StackOverflow-lite website'), 200

@app.route('/signup', methods=['POST'])
def create_a_user_account():
    data = request.get_json()
    username = str(data.get("username"))
    firstname = str(data.get("firstname"))
    surname = str(data.get("surname"))
    email = str(data.get("email"))
    get_pass = str(data.get("password"))
    if request.method == 'POST':
        try:
            if not data or data == "None" or len(data) == 0:
                return make_response(jsonify({"status":-1, "message":"REQUIRED FIELD: Don't leave blank or submit spaces!"})), 400
            
            if len(get_pass) <= 6  or (get_pass.isalpha and get_pass.isdigit()):
                return make_response(jsonify({"status":-1, "message":"Password not strong enough: Requires atleast 6 alphanumeric characters!"})), 406
    
            database.create_new_user(username, firstname, surname, email, get_pass)
            return make_response(jsonify({"status":1, "message":"Success", "records":"Welcome %s Sign Up Successfull"% (username)})), 201
        except:
            return make_response(jsonify({"status":-1, "message":"Username/email already exists! Try again"})), 409

@app.route('/auth/login', methods=['POST'])
def login_a_user():
    #auth = request.authorization
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if request.method == 'POST':
        if username in database.extract_all_users().keys():
            if sha256_crypt.verify(password, database.extract_all_users()[username]["password"]):
                token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
                return make_response(jsonify({'status':0, 'message':'Logged in successfully as: %s'% (username),'token': token.decode('UTF-8')})), 200
            else:
                return make_response(jsonify({"status":-1, "message":"Password is incorrect, try again"})), 400
        else:
            return make_response(jsonify({"status":-2, "message":"Invalid username: %s doesn't exist!" % (username)})), 404

@app.route('/auth/user/questions', methods=['GET'])
@token_required
def view_all_questions_user_asked(current_user):
    if request.method == 'GET':
        if len(database.get_all_users_questions(current_user).keys()) == 0:
            return make_response(jsonify({"status":-2, "message": "No available questions by current user."})), 404
        
        users_questions = database.get_all_users_questions(current_user)
        return make_response(jsonify({"status":0, "message":"Success", "records":users_questions})), 200

@app.route('/questions', methods=['GET'])
def view_all_questions():
    if request.method == 'GET':
        if len(database.get_all_questions().keys()) <= 0:
            return make_response(jsonify({"status":-2, "message":"No available questions to display"})), 404
        
        all_questions = database.get_all_questions()
        return make_response(jsonify({"status":0, "message":"Success", "records":all_questions})), 200

@app.route('/questions', methods=['POST'])
@token_required
def add_question(current_user):
    data = request.get_json()
    username = current_user
    title = str(data.get("title"))
    description = str(data.get("description"))
    error = "Unable to add question due to missing/duplicate required fields. Try again."
    if request.method == 'POST':
        try:
            if not data or data == "None" or len(data) == 0:
                return make_response(jsonify({"status":-1, "message":"REQUIRED FIELD: Don't leave blank or submit spaces!"})), 400
            
            posted_answer = stack.add_questions(username, title, description)
            return make_response(jsonify({"status":1, "message":"Success", "records":posted_answer})), 201
        except:
            return make_response(jsonify({"status":-1, "message":error})), 400

@app.route('/questions/<int:questionid>', methods=['GET'])
def view_a_question(questionid):
    if request.method == 'GET':
        try:
            questions = stack.view_question(questionid)
            return make_response(jsonify({"status":0, "message":"Success", "records":questions})), 200
        except:
            return make_response(jsonify({"status":-2, "message":"Question doesn't exist: Check questionID!"})), 404

        
        
        
# API View which is to be used to search for key-words in the database
@app.route('/questions/search', methods=['POST'])

def search_for_a_question():
#   validating if the requested method is a POST
    if request.method == 'POST':

#       obtaining the posted data as a JSON
        data = request.get_json()

#       validating if the key-word that has been sent contains any characters
        if not data or data == "None" or len(data) == 0:
            return make_response(jsonify({"status":-1, "message":"EMPTY field"})), 400

#       obtaining the key-word string from recieved data
        phrase = str(data.get('search'))

#       validating to check if the user input anything
        if not phrase or phrase == "None" or len(phrase) == 0:
            return make_response(jsonify({"status":-1, "message":"REQUIRED FIELD: Empty search parameter"})), 400

#       returning the results of the search 
        qret = database.search_for_question(phrase)

#       validating if the search returned any results
        if len(qret.keys()) == 0:
            return make_response(jsonify({"status":-2, "message":"Search returned no results."})), 404

#       this runs when the serach returns results and it posts them to the user as a JSON
        return make_response(jsonify({"status":0, "message":"Success", "records":qret})), 200

#   Incase none of the above conditions has been fullfilled, this error code is run
    else:
        abort (405)

@app.route('/questions/max', methods=['GET'])
def view_most_answered_question():
    if request.method == 'GET':
        try:
            result = ans.view_question_with_most_answers()
            return make_response(jsonify({"status":0, "message":"Success", "records":result})), 200
        except:
            return make_response(jsonify({"status":-2, "message":"Question doesn't exist!"})), 400

@app.route('/questions/<int:questionid>', methods=['DELETE'])
@token_required
def delete_a_question(current_user, questionid):
    if request.method == 'DELETE':
        if questionid in database.get_all_questions().keys():
            if database.get_all_questions()[questionid]["username"] == current_user:
                database.delete_a_question(questionid)
                return make_response(jsonify({"status":0, "message":"Success"})), 202
            else:
                return make_response(jsonify({"status":-1, "message":"Current user not authorized to delete this question.!"})), 403
        else:
            return make_response(jsonify({"status":-2, "message":"Unable to delete question which doesn't exist: Check questionID!"})), 400
        
@app.route('/questions/<int:questionid>/answers', methods=['POST'])
@token_required
def add_an_answer(current_user, questionid):
    data = request.get_json()
    if request.method == 'POST':
        try:
            username = current_user
            title = str(data.get("title"))
            description = str(data.get("description"))
            if questionid not in database.get_all_questions().keys():
                return make_response(jsonify({"status":-2, "message":"Question not found: Question ID out of range!"})), 404
            
            if (data == None) or (len(data) <= 0) or not data:
                return make_response(jsonify({"status":-1, "message":"REQUIRED FIELD: Don't leave blank or submit spaces!"})), 400
            
            result = ans.add_answer(questionid, username, title, description)
            return make_response(jsonify({"status":1, "message":"Success", "records":result})), 201
        except:
            return make_response(jsonify({"status":-1, "message":"Unable to add answer due to missing/duplicate required fields. Try again."})), 400
    else:
        abort(405)

@app.route('/answers/<int:answerid>/update', methods=['PUT'])
@token_required
def update_an_answer(current_user, answerid):
    data = request.get_json()
    if request.method == 'PUT':
        try:
            new_answer = str(data.get('new_answer'))
            if answerid in database.extract_all_answers().keys():
                if database.extract_all_answers()[answerid]['username'] == current_user:
                    result = jsonify(ans.update_an_answer(answerid, new_answer))
                    return make_response({"status":0, "message":"Success", "records":result}), 200
                else:
                    return make_response(jsonify({"status":-1, "message":"Current user not authorized to delete this question.!"})), 403
        except:
            return make_response(jsonify({"status":-2, "message":"Unable to locate answer: Check answerID"})), 404

@app.route('/answers/<int:answerid>/comment', methods=['POST'])
@token_required
def add_comment_to_answer(current_user, answerid):
    data = request.get_json()
    if request.method == 'POST':
        username = current_user
        comment = data.get("comment")
        try:
            if answerid  not in database.extract_all_answers().keys():
                return make_response(jsonify({"status":-2, "message":"Answer not found: Answer ID out of range!"})), 404
            
            if (data == None) or (len(data) <= 0) or not data:
                return make_response(jsonify({"status":-1, "message":"REQUIRED FIELD: Don't leave blank or submit spaces!"})), 400
            
            result = ans.add_comment_to_answer(username, answerid, comment)
            return make_response(jsonify({"status":1, "message":"Success", "records":result})), 201
        except:
            return make_response(jsonify({"status":-1, "message":"Unable to add comment due to missing/duplicate required fields. Try again."})), 400
    else:
        abort(405)

@app.route('/questions/<int:questionid>/answers/<int:answerid>/up', methods=['PUT'])
@token_required
def upvote_an_answer(current_user, questionid, answerid):
    if request.method == 'PUT':
        if questionid in database.get_all_questions().keys():
            if answerid in database.extract_all_answers().keys():
                if database.extract_all_answers()[answerid]["username"] != current_user:
                    database.upvote_answer(answerid)
                    return make_response(jsonify({"status":1, "message":"Success"})), 200
                else:
                    return make_response(jsonify({"status":-1, "message":"Unable to perform operation, lack of access."})), 403
            else:
                return make_response(jsonify({"status":-2, "message":"Unable to locate answer: Check answerID"})), 404
        else:
            return make_response(jsonify({"status":-2, "message":"Failed to locate questionID for requested answer"})), 404

@app.route('/questions/<int:questionid>/answers/<int:answerid>/down', methods=['PUT'])
@token_required
def downvote_an_answer(current_user, questionid, answerid):
    if request.method == 'PUT':
        if questionid in database.get_all_questions().keys():
            if answerid in database.extract_all_answers().keys():
                if database.extract_all_answers()[answerid]["username"] != current_user:
                    database.downvote_answer(answerid)
                    return make_response(jsonify({"status":1, "message":"Success"})), 200
                else:
                    return make_response(jsonify({"status":-1, "message":"Unable to perform operation, lack of access."})), 403
            else:
                return make_response(jsonify({"status":-2, "message":"Unable to locate answer: Check answerID"})), 404
        else:
            return make_response(jsonify({"status":-2, "message":"Failed to locate questionID for requested answer"})), 404

@app.errorhandler(404)
def content_not_found(e):
    return make_response(jsonify({"status":-2, "message":"Failed to locate requested content"})), 404

@app.route('/questions/<int:questionid>/answers/<int:answerid>', methods=['PUT'])
@token_required
def set_as_preferred_answer(current_user, questionid, answerid):
    if request.method == 'PUT':
        if questionid in database.get_all_questions().keys():
            if answerid in database.extract_all_answers().keys():
                if database.get_all_questions()[questionid]["username"] == current_user:
                    database.select_answer_as_preferred_answer(answerid)
                    return make_response(jsonify({"status":1, "message":"Success"})), 200
                else:
                    return make_response(jsonify({"status":-1, "message":"Unable to perform operation, lack of access."})), 403
            else:
                return make_response(jsonify({"status":-2, "message":"Unable to locate answer: Check answerID"})), 400
        else:
            return make_response(jsonify({"status":-2, "message":"Failed to locate questionID for requested answer"})), 400

if __name__ == '__main__':
    app.run(debug=True)
