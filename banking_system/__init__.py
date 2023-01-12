from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Xfzef78_azea_78azr8a5zr8azr"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost:3306/banking"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from banking_system import routes