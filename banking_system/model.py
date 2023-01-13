from banking_system import db
import hashlib    

class Account(db.Model):    
    __tablename__ = 'accounts' 

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(255))
    iban = db.Column(db.Integer,unique=True)
    amount = db.Column(db.Integer)
    def __init__(self,username,password,amount, iban):
        self.username = username
        self.password = password
        self.amount = amount
        self.iban = iban

    def hashing(password):
        db_password = password
        hash = hashlib.md5(db_password.encode())
        hashing_password = hash.hexdigest()             
        return hashing_password