from flask import Flask,render_template, Response, jsonify
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
app, db = create_app()

#Dictionary to store music file information
def return_dict():
    dict_here = [
        {'id': 1, 'name': 'Acoustic Breeze', 'link': 'music/acousticbreeze.mp3', 'genre': 'General', 'chill out': 5},
        {'id': 2, 'name': 'Happy Rock','link': 'music/happyrock.mp3', 'genre': 'Bollywood', 'rating': 4},
        {'id': 300, 'name': 'Ukulele', 'link': 'music/ukulele.mp3', 'genre': 'Bollywood', 'rating': 4}
        ]
    return dict_here

#Route to render GUI
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def handle_login_data():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    x = login_gest(username, password, db)
    if x == 'FAILURE':
        return render_template('login.html')
    else :
        return (show_entries())

@app.route('/login', methods=['POST'])
def show_entries():
    general_Data = {
        'title': 'Music Player'}
    #print(return_dict())
    stream_entries = return_dict()
    return render_template('simple.html', entries=stream_entries, **general_Data)

#Route to stream music
@app.route('/<int:stream_id>')
def streammp3(stream_id):
    def generate():
        data = return_dict()
        count = 1
        for item in data:
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

#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server on port : " + str(port))
    http_server.listen(port)
    IOLoop.instance().start()