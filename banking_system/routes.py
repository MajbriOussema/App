from flask import render_template, request, json, Response,flash,redirect,session
from banking_system import app, db
from flask import url_for
from banking_system.model import *
import uuid


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
            hashpassword = Account.hashing(password)
            user_obj = Account.query.filter_by(username=username,password=hashpassword).first()            
            if user_obj:
                user_obj = Account.query.filter_by(username=username,password=hashpassword).first()            
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
            user_exists = Account.query.filter_by(username=username).count()            
            if not user_exists:
                encrypt_password = Account.hashing(password)
                iban = uuid.uuid4().int & (1<<64)-1
                user_obj = Account(username,encrypt_password,100, iban)
                db.session.add(user_obj)
                db.session.commit() 
                session['username'] = user_obj.username
                return redirect(url_for('dashboard'))
            else:
                registerresponse = "Username is already present please choose another"
        else:
            registerresponse = "You must provide a username and a password"
        return render_template('register.html', registerresponse=registerresponse)

@app.route('/sendtrx',methods=['GET','POST'])
def send_transaction():
    if session.get('username'):
        return render_template('sendtrx.html')
    return redirect(url_for('login'))


@app.route('/logout',methods=['GET','POST'])
def logout():
    if session.get('username'):
        session['username'] = None
    return redirect(url_for('login'))

