from flask import Flask, request, jsonify, abort, make_response
from .models import Questions, Answers

app = Flask(__name__)

stack = Questions()
ans = Answers()

@app.errorhandler(400)
def page_not_found(e):
    return make_response(jsonify("Invalid Input/Bad Request, please try again!")), 400

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return jsonify('Welcome to the StackOverflow-lite website')

@app.route('/questions', methods=['GET'])
def view_all_questions():
    if request.method == 'GET':
        """if len(stack.view_questions().keys()) <= 0:
            return make_response(jsonify("No available questions to display")), 404
        else:"""
        return jsonify(stack.view_questions()), 200

@app.route('/questions', methods=['POST'])
def add_question():
    data = request.get_json()
    user_id = str(data.get("user_id"))
    title = str(data.get("title"))
    description = str(data.get("description"))
    question = [user_id, title, description]
    if request.method == 'POST':
        """if question.isspace() or question == "None" or len(question) <=0:
            return make_response(jsonify("REQUIRED FIELD: Don't leave blank or submit spaces!")), 400
        elif question.isnumeric() :
            return make_response(jsonify("Invalid Input, please try again!")), 400
        else:"""
        return jsonify(stack.add_questions(user_id, title, description)), 201

@app.route('/questions/<int:questionid>', methods=['GET'])
def view_a_question(questionid):
    if request.method == 'GET':
        return jsonify(stack.view_question(questionid)), 200

@app.route('/questions/<int:questionid>', methods=['DELETE'])
def delete_a_question(questionid):
    if request.method == 'DELETE':
        return jsonify(stack.delete_question(questionid))
        
@app.route('/questions/<int:questionid>/answers', methods=['POST'])
def add_an_answer(questionid):
    data = request.get_json()
    if request.method == 'POST':
        qid = str(data.get("qid"))
        user_id = str(data.get("user_id"))
        title = str(data.get("title"))
        description = str(data.get("description"))
        answer = [qid, user_id, title, description]
        """if questionid not in stack.questions.keys():
            return make_response(jsonify("Question not found: Question ID out of range!")), 404
        elif answer.isdigit():
            return make_response(jsonify("Invalid Input, please try again!")), 400
        elif (answer == None) or (len(answer) <= 0) or answer.isspace():
            return make_response(jsonify("REQUIRED FIELD: Don't leave blank or submit spaces!")), 400
        else:"""
        return jsonify(ans.add_answer(qid, user_id, title, description)), 201
    else:
        abort(405)

@app.errorhandler(404)
def content_not_found(e):
    return make_response(jsonify("Failed to locate questionID with requested answer")), 404

@app.route('/questions/<int:questionid>/answers', methods=['GET'])
def view_answers(questionid):
    if request.method == 'GET':
        return jsonify(ans.view_answers(questionid)), 200

@app.route('/questions/<int:questionid>/answers/<int:answerid>', methods=['POST'])
def set_as_preferred_answer(self, questionid, answerid):
    if request.method == 'POST':
        return jsonify(ans.select_preferred_answer(answerid)), 200

    pass

if __name__ == '__main__':
    app.run(debug=True)