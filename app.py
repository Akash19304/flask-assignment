from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
from config import MONGO_URI

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
app.secret_key = 'SECRET'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user = mongo.db.users.find_one({'username': username})
        if user:
            flash('Username already exists!')
            return redirect(url_for('signup'))

        mongo.db.users.insert_one({'username': username, 'password': hashed_password})
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = mongo.db.users.find_one({'username': username})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('welcome'))

        flash('Invalid username or password')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return f'Hello Geeks, {session["username"]}!'
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
