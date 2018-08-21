import unittest
import pytest
from app.questions import Questions

class TestForQuestions(unittest.TestCase):
    def setUp(self):
        self.quest = Questions()
        
    def test_if_question_is_added(self):
        question = self.quest.add_questions('What is a boolean')
        assert isinstance(question,  type())

    def test_if_questions_can_be_viewed(self):
        assert isinstance(self.quest.view_questions(), dict)

    def test_if_a_question_is_viewed(self):
        assert isinstance(self.quest.view_question(1), self.quest.questions.keys())

    def test_if_an_answer_is_added(self):
        self.quest.add_answer(2,'the answer')
        assert len(self.quest.answers) >= 1

    def test_if_answers_are_viewed(self):
        assert isinstance(self.quest.view_answers(1), self.quest.answers.values())

if __name__ == '__main__':
    unittest.main()