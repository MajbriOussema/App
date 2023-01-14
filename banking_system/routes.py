from flask import render_template, request, json, Response,flash,redirect,session
from banking_system import app, db
from flask import url_for
from banking_system.model import *
from sqlalchemy.sql import or_,text

import uuid


@app.route('/',methods=['GET','POST'])
def home():
    if session.get('username'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if session.get('username'):
        amount = session['amount']
        iban = session['iban']
        return render_template('dashboard.html', amount=amount, iban=iban)
    return redirect(url_for('login'))
@app.route('/profile',methods=['GET','POST'])
def profile():
    if session.get('username'):
        if request.method == 'GET':
            return render_template('profile.html')
        username = request.form.get('username',None)
        is_admin = request.form.get('is_admin',None)
        if username:
            user_obj = Account.query.filter_by(username=session['username']).first()
            user_obj.username = username
            session['username'] = username
            if is_admin == "true":
                session['is_admin'] = True
            db.session.commit()
            updateresponse = "Username successfully updated"
        else:
            updateresponse = "You must provide a username"
        return render_template('profile.html', updateresponse=updateresponse)
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
                    session['id'] = user_obj.id
                    session['amount'] = user_obj.amount
                    session['iban'] = user_obj.iban
                    session['is_admin'] = False
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
                session['amount'] = user_obj.amount
                session['iban'] = user_obj.iban
                session['id'] = user_obj.id
                session['is_admin'] = False
                return redirect(url_for('dashboard'))
            else:
                registerresponse = "Username is already present please choose another"
        else:
            registerresponse = "You must provide a username and a password"
        return render_template('register.html', registerresponse=registerresponse)

@app.route('/transactions',methods=['GET'])
def get_transactions():
    if session.get('username'):
        transactions = Transaction.query.filter(or_(Transaction.sender_id==session['id'], Transaction.receiver_iban==session['iban'])).all()
        return render_template('transactions.html', transactions=transactions)
    return redirect(url_for('login'))
@app.route('/checkiban',methods=['GET','POST'])
def check_iban():
    if session.get('username'):
        if request.method == 'GET':
            return render_template('checkiban.html')
        iban = request.form.get('iban',None)
        if iban:
            iban_check = Account.query.filter(text("iban='{}'".format(iban))).first()
            if iban_check:
                checkibanresponse = "iban does exist"
            else:
                checkibanresponse = "iban doesn't exist"
        else:
            checkibanresponse = "You must provide an iban "
        return render_template('checkiban.html', checkibanresponse=checkibanresponse)
    return redirect(url_for('login'))
@app.route('/sendtrx',methods=['GET','POST'])
def send_transaction():
    if session.get('username'):
        if request.method == 'GET':
            return render_template('sendtrx.html')
        iban = request.form.get('iban',None) 
        amount = request.form.get('amount',None)
        description = request.form.get('description',None)
        if iban and amount and description:
            user_exists = Account.query.filter_by(iban=iban).count()
            if user_exists:
                if amount.isnumeric() and int(amount) <= int(session['amount']):
                    trx_obj = Transaction(session['id'], iban, amount, description)
                    rcv = Account.query.filter_by(iban=iban).first()
                    snd = Account.query.filter_by(id=session['id']).first()
                    rcv.amount = int(rcv.amount) + int(amount)
                    snd.amount = int(session['amount']) - int(amount)
                    session['amount'] = snd.amount
                    db.session.add(trx_obj)
                    db.session.commit() 
                    return redirect(url_for('dashboard'))
                else:
                    sendtrxresponse = "you don't have the amount"
            else:
                sendtrxresponse = "receiver doesn't exist, please check the IBAN"
        else:
            sendtrxresponse = "You must provide an iban and an amount and description"
        return render_template('sendtrx.html', sendtrxresponse=sendtrxresponse)
    return redirect(url_for('login'))

@app.route('/admin',methods=['GET','POST'])
def admin():
    if session.get('username'):
        if session['is_admin'] == True:
            return render_template('admin.html')
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/admin/getcustomers',methods=['GET','POST'])
def getcustomers():
    if session.get('username'):
        if session['is_admin'] == True:
            if request.method == 'GET':        
                return render_template('customers.html',user=None)
            username = request.form.get('username',None)
            if username:
                user = [u.__dict__  for u in Account.query.filter(text("username='{}'".format(username))).all()]
                searchresponse="success"
            else:
                user = None
                searchresponse="You must provide a username"
            return render_template('customers.html',searchresponse=searchresponse,user=user)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
@app.route('/logout',methods=['GET','POST'])
def logout():
    if session.get('username'):
        session['username'] = None
    return redirect(url_for('login'))

