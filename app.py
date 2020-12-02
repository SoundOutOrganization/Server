from flask import Flask,render_template, Response, jsonify, redirect
import sys
import flask
from init import *
from auth import *
from debug import init_logs_formatting
import logging
# Tornado web server imports
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_sqlalchemy import SQLAlchemy
import json

init_logs_formatting()
app, db= create_app()

#add music to db
@app.route('/addmusic')
def template_addmusic():
    return render_template('addmusic.html')
@app.route('/addmusic', methods=['POST'])
def test_music_db():
    genre = request.form.get('genre')
    title = request.form.get('title')
    author = request.form.get('author')
    link = request.form.get('link')
    new_single = Musics(genre=genre, title=title, author=author, link="music/"+ link)
    db.session.add(new_single)
    db.session.commit()
    return redirect("http://localhost:5000/addmusic", code=302)

def get_musics_dict():
    x = 1
    value = []
    while(x != Musics.query.count()):
        new_single =  Musics.query.get(x)
        print (x)
        value.append({'id': x, 'genre': new_single.genre, 'title': new_single.title, 'author': new_single.author, 'link': new_single.link})
        x +=1
    return (value)

#Route to render GUI

@app.route('/musics')
def get_musics_route():
    x = 1
    value = []
    while(x != Musics.query.count()):
        new_single =  Musics.query.get(x)
        print (x)
        value.append({'id': x, 'genre': new_single.genre, 'title': new_single.title, 'author': new_single.author, 'link': new_single.link})
        x +=1
    return (jsonify(value))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login_data():
    username = request.form.get('username')
    password = request.form.get('password')
    x = login_gest(username, password, db)
    print(x)
    if x == "FAILURE":
        return render_template('login.html')
    else :
        return redirect("http://localhost:5000/addmusic", code=302)

#Route to stream music
@app.route('/play/<int:stream_id>')
def streammp3(stream_id):
    def generate():
        data = get_musics_dict()
        count = 1
        for item in data:
            print(item['id'])
            if item['id'] == stream_id:
                song = item['link']
        with open(song, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
                logging.debug('Music data fragment : ' + str(count))
                count += 1
                
    return Response(generate(), mimetype="audio/mp3")

@app.route('/')
def main_route():
    return redirect("http://localhost:5000/login", code=302)

#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    db.create_all() 
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server on port : " + str(port))
    http_server.listen(port)
    IOLoop.instance().start()