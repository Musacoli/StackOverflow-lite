# StackOverflow-lite

StackOverflow lite is a platform where users are able to ask questions, receive answers and select or upvote which answer best suited the question asked.


Link to Hosted Version on Heroku
(<https://stackoverflow-lite-collo.herokuapp.com/)>

[![Build Status](https://travis-ci.org/Musacoli/StackOverflow-lite.svg?branch=test_app)](https://travis-ci.org/Musacoli/StackOverflow-lite)

[![Maintainability](https://api.codeclimate.com/v1/badges/1445d14d10d76b542495/maintainability)](https://codeclimate.com/github/Musacoli/StackOverflow-lite/maintainability)

[![Coverage Status](https://coveralls.io/repos/github/Musacoli/StackOverflow-lite/badge.svg?branch=test_app)](https://coveralls.io/github/Musacoli/StackOverflow-lite?branch=test_app)

[![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/codeclimate/codeclimate/test_coverage)


Basic Abbreviations used:
aid = answer_id
qid = question_id
cur = cursor
conn = connection
uid = userid/username


STACKOVERFLOW-LITE API MANUAL

When loading the site for the  first time visit (
 * (<http://127.0.0.1:5000/)>

In order to create a user account that enables you post questions and answers visit:
(<http://127.0.0.1:5000/signup)>

When logging in visit :
(<http://127.0.0.1:5000/auth/kogin)>

When needing to view all questions without having logged in, visit:
(<http://127.0.0.1:5000/questions)>

To view all questions that a user has asked/posted before visit:
(<http://127.0.0.1:5000/auth/user/questions)>
