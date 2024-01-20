import flask
from flask import Flask
from flask import render_template
from flask import request

from PIL import Image

from run import inference_image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/imagenet', methods=['POST'])
def imagenet():
    image = flask.request.files.get('image')
    image = Image.open(image)
    return inference_image(image)

if __name__ == '__main__':
   app.run()