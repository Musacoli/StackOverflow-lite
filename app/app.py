from flask import Flask, request, jsonify, abort
from .questions import Questions

app = Flask(__name__)

stack = Questions()

@app.route('/', methods=['GET', 'POST'])
def hello():
    return jsonify('Hello there!')

@app.route('/questions', methods=['GET'])
def view_all_questions():
    if request.method == 'GET':
        return jsonify(stack.view_questions()), 201
    else:
        abort(405)

@app.route('/questions', methods=['POST'])
def add_question():
    if request.method == 'POST':
        return jsonify(stack.add_questions('What is a boolean?')), 201
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
    if request.method == 'POST':
        return jsonify(stack.add_answer(questionid, 'This is the most correct answer'))
    elif request.method == 'GET':
        return jsonify(stack.view_answers(questionid))
    else:
        abort(405)

if __name__ == '__main__':
    app.run(debug=True)