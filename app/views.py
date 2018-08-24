from flask import Flask, request, jsonify, abort, make_response
from models import Questions, Answers

app = Flask(__name__)

stack = Questions()
ans = Answers()

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return jsonify('Welcome to the StackOverflow-lite website')

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
    question = str(data.get("question"))
    if request.method == 'POST':
        if question.isdigit():
            return make_response(jsonify("Invalid Input, please try again!")), 400
        elif (question == None) or (len(question) <= 0) or question.isspace():
            return make_response(jsonify("REQUIRED FIELD: Don't leave blank or submit spaces!")), 400
        else:
            return jsonify(stack.add_questions(question)), 201

@app.route('/questions/<int:questionid>', methods=['GET'])
def view_a_question(questionid):
    if request.method == 'GET':
        return jsonify(stack.view_question(questionid)), 201
        
@app.route('/questions/<int:questionid>/answers', methods=['POST'])
def add_an_answer(questionid):
    data = request.get_json()
    if request.method == 'POST':
        answer = str(data.get("answer"))
        if questionid not in stack.questions.keys():
            return make_response(jsonify("Question not found: Question ID out of range!")), 404
        elif answer.isdigit():
            return make_response(jsonify("Invalid Input, please try again!")), 400
        elif (answer == None) or (len(answer) <= 0) or answer.isspace():
            return make_response(jsonify("REQUIRED FIELD: Don't leave blank or submit spaces!")), 400
        else:
            return jsonify(ans.add_answer(questionid, answer))
    else:
        abort(405)

@app.route('/questions/<int:questionid>/answers', methods=['GET'])
def view_answers(questionid):
    if request.method == 'GET':
        if questionid in stack.questions.keys():
            return jsonify(ans.view_answers(questionid))
        else:
            return make_response(jsonify("Failed to locate question to answer")), 404

if __name__ == '__main__':
    app.run(debug=True)