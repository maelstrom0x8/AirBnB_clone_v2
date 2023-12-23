#!/usr/bin/python3

from flask import Flask, render_template

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

@app.route("/number/<int:n>", strict_slashes=False)
def message_number(n: int):
    return f"{n} is a number"

@app.route('/number_template/<int:n>')
def number_template(n: int):
    return render_template("5-number.html", number=n)

@app.route('/number_odd_or_even/<int:n>')
def number_template_odd(n: int):
    b = 'odd'
    if n % 2 == 0 :
        b = 'even'

    return render_template("6-number_odd_or_even.html", n=n, b=b)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
