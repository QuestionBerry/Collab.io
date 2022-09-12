from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/new/user', methods=['POST'])
def create_user():
    if User.validate(request.form):
        hashed_password = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'email' : request.form['email'],
            'username' : request.form['username'],
            'password' : hashed_password
        }
        session['user_id'] = User.create(data)
        return redirect('/queues/clients')
    else:
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    user = User.readOneByUsername(request.form)
    if not user:
        flash('Username not found', 'login')
        return redirect('/')
    if not request.form['password']:
        flash('Enter Password', 'login')
        return redirect('/')
    else:
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Incorrect Password', 'login')
            return redirect('/')
        else:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/queues/clients')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
