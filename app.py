from flask import Flask,render_template, Response, jsonify, redirect
import sys
import flask
from init import *
from auth import *
from debug import init_logs_formatting
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import logging
import json
import os
init_logs_formatting()
app, db= create_app()
app.config['UPLOAD_PATH'] = 'music'
#app.config['MAX_CONTENT_PATH']
app.config['UPLOAD_EXTENSIONS'] = ['.mp3', '.wav']         #if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:abort(400)

#add music to db
@app.route('/addmusic')
def template_addmusic():
    return render_template('addmusic.html')

@app.route('/addmusic', methods=['POST'])
def test_music_db():
    genre = request.form.get('genre')
    title = request.form.get('title')
    author = request.form.get('author')
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        file_name = os.path.splitext(filename)[0]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            print("test")
        else:
            new_single = Musics(genre=genre, title=title, author=author, link="music/"+ file_name + file_ext)
            db.session.add(new_single)
            db.session.commit()
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    return redirect("http://localhost:5000/addmusic", code=302)

def get_musics_dict():
    x = 1
    value = []
    while(x <= Musics.query.count()):
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
    while(x <= Musics.query.count()):
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
    #print(x)
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
    logging.debug("Started Server on port : " + str(port))
    app.run(host='0.0.0.0')