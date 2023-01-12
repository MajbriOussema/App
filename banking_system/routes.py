from flask import render_template, request, json, Response,flash,redirect,session
from banking_system import app, db
from flask import url_for
from banking_system.model import *

@app.route('/',methods=['GET','POST'])
def home():
    if session.get('username'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if session.get('username'):
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    formData = dict()
    if session.get('username'):
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username',None) 
        password = request.form.get('password',None)
        formData['username'] = username
        formData['password'] = password
        if username and password:
            hashpassword = UserRegistration.hashing(password)
            user_obj = UserRegistration.query.filter_by(username=username,password=hashpassword).first()            
            if user_obj:
                user_obj = UserRegistration.query.filter_by(username=username,password=hashpassword).first()            
                if user_obj:
                    session['username'] = user_obj.username
                    return redirect(url_for('dashboard'))
                else:
                    loginresponse = "Password is invalid"
            else:
                loginresponse = "Username is invalid"
        else:
            loginersponse = "You must provide a username and a password"

    return render_template('login.html', loginresponse=loginresponse)

@app.route('/register',methods=['GET','POST'])
def register():
    formData = dict()
    if session.get('username'):
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username',None) 
        password = request.form.get('password',None)
        if username and password:
            user_exists = UserRegistration.query.filter_by(username=username).count()            
            if not user_exists:
                encrypt_password = UserRegistration.hashing(password)
                user_obj = UserRegistration(username,encrypt_password)
                db.session.add(user_obj)
                db.session.commit() 
                session['username'] = user_obj.username
                return redirect(url_for('dashboard'))
            else:
                registerresponse = "Username is already present please choose another"
        else:
            registerresponse = "You must provide a username and a password"
        return render_template('register.html', registerresponse=registerresponse)