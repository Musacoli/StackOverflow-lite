import unittest
import pytest
from app.questions import Questions

class TestForQuestions(unittest.TestCase):
    def setUp(self):
        self.quest = Questions()

    def test_if_question_is_added(self):
        assert isinstance(self.quest.add_questions('What is a boolean'),  dict)

    def test_if_questions_can_be_viewed(self):
        assert isinstance(self.quest.view_questions(), dict)

    def test_if_a_question_is_viewed(self):
        self.quest.add_questions('What is a boolean')
        assert isinstance(self.quest.view_question(1), dict)

    def test_if_an_answer_is_added(self):
        self.quest.add_questions('What is a boolean')
        assert isinstance(self.quest.add_answer(1,'the answer'), dict)

    def test_if_answers_are_viewed(self):
        self.quest.add_questions('What is a boolean')
        self.quest.add_answer(1,'the answer')
        assert isinstance(self.quest.view_answers(1), dict)

if __name__ == '__main__':
    unittest.main()
