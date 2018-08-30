from flask import Flask, request, jsonify, abort, make_response
from app.models import Users, Questions, Answers
from passlib.hash import sha256_crypt


app = Flask(__name__)

user = Users()
stack = Questions()
ans = Answers()

@app.errorhandler(400)
def page_not_found(e):
    return make_response(jsonify("Invalid Input/Bad Request, please try again!")), 400

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return jsonify('Welcome to the StackOverflow-lite website')

@app.route('/signup', methods=['POST'])
def create_a_user_accout():
    data = request.get_json()
    user_id = str(data.get("user_id"))
    firstname = str(data.get("firstname"))
    surname = str(data.get("surname"))
    email = str(data.get("email"))
    password = sha256_crypt.encrypt(str(data.get("password")))
    if request.method == 'POST':
        try:
            if not data or data == "None" or len(data) == 0:
                return make_response(jsonify("REQUIRED FIELD: Don't leave blank or submit spaces!")), 400
            else:
                return jsonify(user.add_user_account(user_id, firstname, surname, email, password)), 201
        except:
            return make_response(jsonify("User_ID/email already exists! Try again")), 400

@app.route('/login', methods=['POST'])
def login_a_user():
    data = request.get_json()
    user_id = data.get("user_id")
    password = data.get("password")
    if request.method == 'POST':
        if user_id in user.users.keys():
            if sha256_crypt.verify(password, user.users[user_id]["password"]):
                return make_response(jsonify("User: %s has logged in successfully!" % (user_id))), 200
            else:
                return make_response(jsonify("Password is incorrect, try again")), 400
        else:
            return make_response(jsonify("Invalid username: Username doesn't exist!")), 400

@app.route('/questions', methods=['GET'])
def view_all_questions():
    if request.method == 'GET':
        if len(stack.view_questions().keys()) <= 0:
            return make_response(jsonify("No available questions to display")), 404
        else:
            return jsonify(stack.view_questions()), 200

@app.route('/questions', methods=['POST'])
def add_question():
    data = request.get_json()
    user_id = str(data.get("user_id"))
    title = str(data.get("title"))
    description = str(data.get("description"))
    error = "Unable to add question due to missing/duplicate required fields. Try again."
    if request.method == 'POST':
        try:
            if not data or data == "None" or len(data) == 0:
                return make_response(jsonify("REQUIRED FIELD: Don't leave blank or submit spaces!")), 400
            else:
                return jsonify(stack.add_questions(user_id, title, description)), 201
        except:
            return make_response(jsonify(error)), 400

@app.route('/questions/<int:questionid>', methods=['GET'])
def view_a_question(questionid):
    if request.method == 'GET':
        try:
            return jsonify(stack.view_question(questionid)), 200
        except:
            return make_response(jsonify("Question doesn't exist: Check questionID!")), 400

@app.route('/questions/<int:questionid>', methods=['DELETE'])
def delete_a_question(questionid):
    if request.method == 'DELETE':
        if questionid in stack.questions.keys():
            return jsonify(stack.delete_question(questionid)), 202
        else:
            return make_response(jsonify("Unable to delete question which doesn't exist: Check questionID!")), 400
        
@app.route('/questions/<int:questionid>/answers', methods=['POST'])
def add_an_answer(questionid):
    data = request.get_json()
    error = "Unable to add answer due to missing/duplicate required fields. Try again."
    if request.method == 'POST':
        try:
            user_id = str(data.get("user_id"))
            title = str(data.get("title"))
            description = str(data.get("description"))
            if questionid not in stack.questions.keys():
                return make_response(jsonify("Question not found: Question ID out of range!")), 404
            elif (data == None) or (len(data) <= 0) or not data:
                return make_response(jsonify("REQUIRED FIELD: Don't leave blank or submit spaces!")), 400
            else:
                return jsonify(ans.add_answer(questionid, user_id, title, description)), 201
        except:
            return make_response(jsonify(error)), 400
    else:
        abort(405)

@app.errorhandler(404)
def content_not_found(e):
    return make_response(jsonify("Failed to locate questionID with requested answer")), 404

@app.route('/questions/<int:questionid>/answers/<int:answerid>', methods=['POST'])
def set_as_preferred_answer(questionid, answerid):
    if request.method == 'POST':
        if questionid in stack.questions.keys():
            if answerid in ans.answers.keys():
                return jsonify(ans.select_preferred_answer(answerid)), 201
            else:
                return make_response(jsonify("Unable to locate answer: Check answerID")), 400
        else:
            return make_response(jsonify("Failed to locate questionID for requested answer")), 400

if __name__ == '__main__':
    app.run(debug=True)