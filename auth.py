from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required
from init import Users
#from werkzeug.security import generate_password_hash, check_password_hash

def login_gest(username, password, db):
    test_user = Users.query.filter_by(user=username).first()
    print ("tesdzdzdzdzdzdzdzdzdzdzdzdzdzdzdzdzdzdzdz")
    if(test_user != None):
        print(test_user.user,"-> [USER EXIST]", flush=True)
        if(test_user.passw != password):
            print(password,"-> [INCORRECT PASSWORD]", flush=True)
            return("FAILURE")
        elif(test_user.passw == password):
            print("[CONNECTION OK]", flush=True)
            value = {'username': test_user.user, 'password': test_user.passw}
            return (jsonify(value))
    elif(test_user == None):
        new_user = Users(user=username, passw=password)
        db.session.add(new_user)
        db.session.commit()
        print(new_user.user,"-> [USER CREATED]\n[CONNECTION OK]", flush=True)
        value = {'username': new_user.user, 'password': new_user.passw}
        return (jsonify(value))