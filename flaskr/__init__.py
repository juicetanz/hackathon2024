import flask
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for

import sqlite3

from PIL import Image

from run import inference_image
from . import db
from flaskr.templates.cropprediction.run import run_suggestion

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = Flask.secret_key
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import open_db, create_user, check_user_pass, create_crop, set_current_user, get_crops
    open_db("data.json")

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/newcrop', methods=['POST'])
    def newcrop():
        image = flask.request.files.get('image')
        name = flask.request.form['name']
        val = flask.request.form['val']
        create_crop(name, image, val)
        return ""

    @app.route('/imagenet', methods=['POST'])
    def imagenet():
        image = flask.request.files.get('image')
        image = Image.open(image)
        res = inference_image(image)
        return res[0]
    
    @app.route('/prediction', methods=['GET','POST'])
    def prediction():
        if request.method == 'POST':
            n = request.form['n']
            p = request.form['p']
            k = request.form['k']
            temp = request.form['temp']
            humid = request.form['humid']
            ph = request.form['ph']
            rain = request.form['rain']
            return run_suggestion(n,p,k,temp,humid,ph,rain)

        return render_template('cropprediction/prediction.html')

    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            
            create_user(username, password)
            set_current_user(username)
            return redirect('/')
        return render_template('auth/register.html')
    
    @app.route('/loadcrops', methods=['GET'])
    def loadcrops():
        return get_crops()

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']

            passed = check_user_pass(username, password)

            if passed:
                # Create session data, we can access this data in other routes
                set_current_user(username)
                # Redirect to home page
                return redirect('/')
            else:
                # Account doesnt exist or username/password incorrect
                print("STUID NOT IN")
                return redirect('/login')
        return render_template('auth/login.html')
    
    '''
            <form method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
    '''
    
    @app.route('/logout')
    def logout():
        # remove the username from the session if it's there
        set_current_user("")
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run()

    return app