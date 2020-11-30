import flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask.
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'
db = SQLAlchemy(app)

class Users(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   user = db.Column(db.String(100))
   passw = db.Column(db.String(100))

def __init__(self, user, passw):
   self.user = user
   self.passw = passw

def create_app():
   return(app, db)