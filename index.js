
var express = require('express');
var app = express();
var path = require('path');

app.use(express.static(path.join(__dirname)));
app.use("UI/css", express.static(__dirname + 'UI/css'));
app.use("UI/images", express.static(__dirname + 'UI/images'));
app.use("UI/scripts", express.static(__dirname + 'UI/scripts'));
app.use("UI/html", express.static(__dirname + 'UI/html'));

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname + 'index.html'));
});

app.get('/signup', function (req, res) {
  res.sendFile(path.join(__dirname + 'html/signup.html'));
});

app.get('/auth/login', function (req, res) {
    res.sendFile(path.join(__dirname + 'html/login.html'));
});

app.get('/auth/users/questions', function (req, res) {
    res.sendFile(path.join(__dirname + 'html/profile.html'));
});

app.get('/questions', function (req, res) {
    res.sendFile(path.join(__dirname + 'html/question_form.html'));
});

app.get('/answers', function (req, res) {
    res.sendFile(path.join(__dirname + 'html/answer_form.html'));
});

app.get('/comments', function (req, res) {
    res.sendFile(path.join(__dirname + 'html/comment.html'));
  });

app.listen(process.env.PORT || 8080);