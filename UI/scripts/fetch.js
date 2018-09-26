
document.getElementById('output').addEventListener('click', getQuestions);
document.getElementById('signup_form').addEventListener('submit', signUp);
document.getElementById('login_form').addEventListener('submit', login);


function getQuestions() {
   // let headers = new Headers();

   // headers.append('Access-Control-Allow-Origin', '*');
   //  headers.append('Access-Control-Allow-Credentials', 'true');
   //  headers.append('Accept', 'application/json, text/plain, */*')
<<<<<<< HEAD
   fetch('https://stackoverflow-lite-collo.herokuapp.com/questions') 
=======
<<<<<<< HEAD
   fetch('https://stackoverflow-lite-collo.herokuapp.com/questions') 
=======
   fetch('http://127.0.0.1:5000/questions') 
>>>>>>> 820f4501a78258999d7daf44736dbeb34722aa3a
>>>>>>> c4f15d8156a666d3e993211ca2b04ef158c7fb37
   .then((res) => res.json())
   .then ((data) => {
       console.log(data);
       let output = '<h3>Questions</h3>';
       Object.values(data['records']).forEach(function(question){
           let qid = 0
           qid++
           output += `
               <div class="r1">
                   <h1>Question</h1>
                   <h3>Title: ${question.question_title}</h3>
                   <p>Description: ${question.description}</p>
                   <br>Time: ${question.post_time}
                   <br>Posted By: ${question.username}
           </div>`;
       });
       
       document.getElementById('test').innerHTML = output;
   })
}

function signUp(e) {
    e.preventDefault();

    let firstname = document.getElementById('firstname').value;
    let surname = document.getElementById('surname').value;
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let cemail = document.getElementById('cemail').value;
    let password = document.getElementById('password').value;
    let cpassword = document.getElementById('cpassword').value;

<<<<<<< HEAD
    fetch('https://stackoverflow-lite-collo.herokuapp.com/signup', {
=======
<<<<<<< HEAD
    fetch('https://stackoverflow-lite-collo.herokuapp.com/signup', {
=======
    fetch('http://127.0.0.1:5000/signup', {
>>>>>>> 820f4501a78258999d7daf44736dbeb34722aa3a
>>>>>>> c4f15d8156a666d3e993211ca2b04ef158c7fb37
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-type': 'application/json'
        },
        body: JSON.stringify({username:username, firstname:firstname, surname:surname, email:email, password:password})
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        if (data['status'] == 1) {
            alert(Object.values(data['records']))
            redirect: window.location.replace("login.html")
        } else {
            alert(Object.values(data['message']))
        }
});
}
     
function login(e) {
    e.preventDefault();

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

<<<<<<< HEAD
    fetch('https://stackoverflow-lite-collo.herokuapp.com/auth/login', {
=======
<<<<<<< HEAD
    fetch('https://stackoverflow-lite-collo.herokuapp.com/auth/login', {
=======
    fetch('http://127.0.0.1:5000/auth/login', {
>>>>>>> 820f4501a78258999d7daf44736dbeb34722aa3a
>>>>>>> c4f15d8156a666d3e993211ca2b04ef158c7fb37
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-type': 'application/json'
        },
        body: JSON.stringify({username:username, password:password})
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        if (data['status'] == 0 ) {
            alert(Object.values(data['message']));
            redirect: window.location.replace("profile.html");
            localStorage.setItem("token", data['token'])
        }
        else {
            alert(Object.values(data['message']));
        }
});
}