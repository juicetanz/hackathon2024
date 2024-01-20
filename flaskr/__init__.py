import flask
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for

from PIL import Image

from run import inference_image

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = Flask.secret_key
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    from . import db
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/imagenet', methods=['POST'])
    def imagenet():
        image = flask.request.files.get('image')
        image = Image.open(image)
        res = inference_image(image)
        return res[0]
    
    @app.route('/prediction')
    def prediction():
        return render_template('cropprediction/prediction.html')

    @app.route('/loginpage')
    def loginpage():
        return render_template('auth/login.html')
    @app.route('/registerpage')
    def registerpage():
        return render_template('auth/register.html')

    @app.route('/login', methods=['POST'])
    def login():
        if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return '''
            <form method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
        '''
    
    @app.route('/logout')
    def logout():
        # remove the username from the session if it's there
        session.pop('username', None)
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run()

    return app