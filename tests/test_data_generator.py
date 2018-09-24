from random import choices
from string import ascii_letters, digits


class TextGenerator(object):

    def user(self):
        return ''.join(choices(ascii_letters + digits, k=5))

    def question(self):
        return ''.join(choices(ascii_letters + ' ', k=40))

    def answer(self):
        return ''.join(choices(ascii_letters + ' ', k=30))

    def comment(self):
        return ''.join(choices(ascii_letters + ' ', k=20))


txt = TextGenerator()

print (type(txt.user()))
