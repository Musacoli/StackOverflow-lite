from flask import Flask, request, jsonify, abort, make_response
from app.models import Users, Questions, Answers
from passlib.hash import sha256_crypt
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config["SECRET_KEY"] = 'thisisstackoverflowlite'

user = Users()
stack = Questions()
ans = Answers()

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
        except:
            return make_response(jsonify({'message': 'Token is invalid'})), 403

        return f(*args, **kwargs)
    return decorated

@app.errorhandler(400)
def page_not_found(e):
    return make_response(jsonify({"message":"Invalid Input/Bad Request, please try again!"})), 400

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return jsonify('Welcome to the StackOverflow-lite website')

@app.route('/signup', methods=['POST'])
def create_a_user_account():
    data = request.get_json()
    username = str(data.get("username"))
    firstname = str(data.get("firstname"))
    surname = str(data.get("surname"))
    email = str(data.get("email"))
    password = sha256_crypt.encrypt(str(data.get("password")))
    if request.method == 'POST':
        try:
            if not data or data == "None" or len(data) == 0:
                return make_response(jsonify({"ERROR!":"REQUIRED FIELD: Don't leave blank or submit spaces!"})), 400
            else:
                return jsonify(user.add_user_account(username, firstname, surname, email, password)), 201
        except:
            return make_response(jsonify({"ERROR!":"Username/email already exists! Try again"}))

@app.route('/login', methods=['POST'])
def login_a_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if request.method == 'POST':
        if username in user.users.keys():
            if sha256_crypt.verify(password, user.users[username]["password"]):
                token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                return make_response(jsonify({'Logged in successfully as:':'User','token': token.decode('UTF-8')})), 200
            else:
                return make_response(jsonify({"ERROR!":"Password is incorrect, try again"})), 400
        else:
            return make_response(jsonify({"ERROR!":"Invalid username: Username doesn't exist!"})), 400

@app.route('/questions', methods=['GET'])
def view_all_questions():
    if request.method == 'GET':
        if len(stack.view_questions().keys()) <= 0:
            return make_response(jsonify({"ERROR!":"No available questions to display"})), 404
        else:
            return jsonify(stack.view_questions()), 200

@app.route('/questions', methods=['POST'])
@token_required
def add_question():
    data = request.get_json()
    username = str(data.get("username"))
    title = str(data.get("title"))
    description = str(data.get("description"))
    error = "Unable to add question due to missing/duplicate required fields. Try again."
    if request.method == 'POST':
        try:
            if not data or data == "None" or len(data) == 0:
                return make_response(jsonify({"ERROR!":"REQUIRED FIELD: Don't leave blank or submit spaces!"})), 400
            else:
                return jsonify(stack.add_questions(username, title, description)), 201
        except:
            return make_response(jsonify({"ERROR!":error})), 400

@app.route('/questions/<int:questionid>', methods=['GET'])
def view_a_question(questionid):
    if request.method == 'GET':
       # try:
        return jsonify(stack.view_question(questionid)), 200
        #except:
            #return make_response(jsonify({"ERROR!":"Question doesn't exist: Check questionID!"})), 400

@app.route('/questions/<int:questionid>', methods=['DELETE'])
@token_required
def delete_a_question(questionid):
    if request.method == 'DELETE':
        if questionid in stack.questions.keys():
            return jsonify(stack.delete_question(questionid)), 202
        else:
            return make_response(jsonify({"ERROR!":"Unable to delete question which doesn't exist: Check questionID!"})), 400
        
@app.route('/questions/<int:questionid>/answers', methods=['POST'])
@token_required
def add_an_answer(questionid):
    data = request.get_json()
    error = "Unable to add answer due to missing/duplicate required fields. Try again."
    if request.method == 'POST':
        try:
            username = str(data.get("username"))
            title = str(data.get("title"))
            description = str(data.get("description"))
            if questionid not in stack.questions.keys():
                return make_response(jsonify({"ERROR!":"Question not found: Question ID out of range!"})), 404
            elif (data == None) or (len(data) <= 0) or not data:
                return make_response(jsonify({"ERROR!":"REQUIRED FIELD: Don't leave blank or submit spaces!"})), 400
            else:
                return jsonify(ans.add_answer(questionid, username, title, description)), 201
        except:
            return make_response(jsonify(error)), 400
    else:
        abort(405)

@app.errorhandler(404)
def content_not_found(e):
    return make_response(jsonify({"ERROR!":"Failed to locate questionID with requested answer"})), 404

@app.route('/questions/<int:questionid>/answers/<int:answerid>', methods=['PUT'])
@token_required
def set_as_preferred_answer(questionid, answerid):
    if request.method == 'PUT':
        if questionid in stack.questions.keys():
            if answerid in ans.answers.keys():
                return jsonify(ans.select_preferred_answer(answerid)), 201
            else:
                return make_response(jsonify({"ERROR!":"Unable to locate answer: Check answerID"})), 400
        else:
            return make_response(jsonify({"ERROR!":"Failed to locate questionID for requested answer"})), 400

if __name__ == '__main__':
    app.run(debug=True)