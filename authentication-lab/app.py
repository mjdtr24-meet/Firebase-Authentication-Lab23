from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'




config = {
  "apiKey": "AIzaSyAaeA35xEen1wCAYEjkr10u6nBbgg42ROs",
  "authDomain": "first-data-base-99ec2.firebaseapp.com",
  "projectId": "first-data-base-99ec2",
  "storageBucket": "first-data-base-99ec2.appspot.com",
  "messagingSenderId": "844525197357",
  "appId": "1:844525197357:web:73b5c401242ed44e3080a4",
  "measurementId": "G-GB7C28FK2S",
  "databaseURL": "https://first-data-base-99ec2-default-rtdb.firebaseio.com/"
}


firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        error = ""
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authenication Error"
            print(error)
            return redirect(url_for('signin'))
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        full_name= request.form['full_name']
        username = request.form['username']     
        bio = request.form ['bio']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"email":email , "password":password , "fullname":full_name ,"username" :username , "bio" :bio}
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except: 
            error = "Authenication Error"
            return redirect(url_for('signin'))
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        uid = login_session['user']['localId']
        title = request.form['title']
        text = request.form['text']
        tweet = {'title': title, 'text': text, 'uid': uid}
        db.child('Tweets').push(tweet)
    return render_template("add_tweet.html")






@app.route('/all_tweets')
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("tweets.html", tweets=tweets)






if __name__ == '__main__':
    app.run(debug=True, port=5001)