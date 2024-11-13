from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expensesDB.db'
app.config['SECRET_KEY'] = 'iashdiafha;sdhfiaasdfadf7\84654871h67873511asdf'

db = SQLAlchemy(app)

from application import routes