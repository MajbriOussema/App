from banking_system import db
import hashlib

class Customer(db.Model):
    __tablename__ = 'customers' 

    id = db.Column(db.Integer,primary_key=True)
    ssn_id = db.Column(db.Integer)    
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))

    def __init__(self,name,ssn_id,address):        
        self.ssn_id = ssn_id
        self.name = name
        self.address = address

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer,primary_key=True) 
    customer_id = db.Column(db.Integer,db.ForeignKey('customers.id'))
    amount = db.Column(db.Integer)
    is_locked = db.Column(db.Boolean,default=False)

    def __init__(self,customer_id,amount):
        self.customer_id = customer_id
        self.amount = amount        

class UserRegistration(db.Model):    
    __tablename__ = 'user_registrations' 

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(255))

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def hashing(password):
        db_password = password
        hash = hashlib.md5(db_password.encode())
        hashing_password = hash.hexdigest()             
        return hashing_password