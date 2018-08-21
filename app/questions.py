import time

class Questions(object):
    
    def __init__(self):
        self.questions = {}
        self.qid = 0
        self.answers = {}

    def add_questions(self, question):
        self.qid += 1
        self.ptime = str(time.ctime())
        if self.qid in self.questions.keys():
            self.qid += 1
            self.questions[self.qid] = {question:self.ptime}
            return self.questions[self.qid]
        else:
            self.questions[self.qid] = {question:self.ptime}
            return self.questions[self.qid]
    
    def view_questions(self):
        return self.questions

    def view_question(self, qid):
        if qid in self.questions.keys():
            return self.questions[qid]
        else:
            return 'Question not found'

    def add_answer(self, qid, answer):
        atime = str(time.ctime())
        if qid in self.questions.keys():
            self.answers[qid] = {answer:atime}
            return self.answers[qid]
        else:
            return 'Failed to find question to comment on'

    def view_answers(self, qid):
        return self.answers[qid]