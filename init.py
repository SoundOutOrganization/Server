import flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask.
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./server.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)
db = SQLAlchemy(app)

class Musics(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   genre = db.Column(db.String(100))
   title = db.Column(db.String(100))
   author = db.Column(db.String(100))
   link = db.Column(db.String(100))

class Users(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   user = db.Column(db.String(100))
   passw = db.Column(db.String(100))

def __init__(self, user, passw, genre, title, author, link):
   self.user = user
   self.passw = passw

   self.genre = genre
   self.title = title
   self.author = author
   self.link = link

def create_app():
   return(app, db)
