from flask import Flask, request, jsonify, abort
from .models import Questions

app = Flask(__name__)

stack = Questions()

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return jsonify('Welcome to the StackOverflow-lite website')

@app.route('/questions', methods=['GET'])
def view_all_questions():
    if request.method == 'GET':
        return jsonify(stack.view_questions()), 201
    else:
        abort(405)

@app.route('/questions', methods=['POST'])
def add_question():
    data = request.get_json()
    question = data.get("question")
    if request.method == 'POST':
        return jsonify(stack.add_questions(question)), 201
    else:
        abort(405)

@app.route('/questions/<int:questionid>', methods=['GET'])
def view_a_question(questionid):
    if request.method == 'GET':
        return jsonify(stack.view_question(questionid))
    else:
        abort(405)

@app.route('/questions/<int:questionid>/answers', methods=['GET','POST'])
def add_an_answer(questionid):
    data = request.get_json()
    if request.method == 'POST':
        answer = data.get("answer")
        return jsonify(stack.add_answer(questionid, answer))
    elif request.method == 'GET':
        return jsonify(stack.view_answers(questionid))
    else:
        abort(405)

if __name__ == '__main__':
    app.run(debug=True)