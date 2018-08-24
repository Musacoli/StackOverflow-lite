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
            for qdict in self.questions.values():
                if question in qdict.keys():
                    return "Duplicate question detected"
                else:
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

class Answers(Questions):
    def add_answer(self, qid, answer):
        atime = str(time.ctime())
        if qid in self.questions.keys():
            self.answers[qid] = {answer:atime}
            return self.answers[qid]
        else:
            return 'Failed to find question to answer'

    def view_answers(self, qid):
        if qid in self.answers.keys():
            return self.answers[qid]
        else:
            return "No answers available to display"

"""test = Questions()

test.add_questions("what")
test.add_questions("who")
test.add_questions("when")
test.add_questions("where")
for qdict in test.questions.values():
    if "what" in qdict.keys():
        print ("True")
        break
    else:
        print ("False")
    print(qdict.keys())"""