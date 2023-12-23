#!/usr/bin/python3

from flask import Flask

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def index():
    return 'Hello HBNB!'

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return 'HBNB'

@app.route("/c/<text>", strict_slashes=False)
def message_c(text: str):
    t = text.replace('_', ' ')
    return 'C ' + t

@app.route("/python/<text>", strict_slashes=False)
@app.route('/python/', strict_slashes=False)
def message_python(text = 'is cool'):
    t = text.replace('_', ' ')
    return 'Python ' + t


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
