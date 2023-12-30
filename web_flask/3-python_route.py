#!/usr/bin/python3

"""
3-python_route.py

This script defines a Flask web application with four routes.

Usage:
- Run the script, and the web application will be accessible at
  http://0.0.0.0:5000.

Routes:
- "/": Displays the message "Hello HBNB!" when accessed.
- "/hbnb": Displays the message "HBNB" when accessed.
- "/c/<text>": Displays the message "C " followed by the value of the 'text'
  variable (underscore '_' symbols replaced with a space).
- "/python/<text>": Displays the message "Python " followed by the value of
  the 'text' variable (underscore '_' symbols replaced with a space).
  The default value of 'text' is "is cool".
"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """
    Route: "/"

    Displays the message "Hello HBNB!" when accessed.

    Returns:
        str: The message "Hello HBNB!".
    """
    return 'Hello HBNB!'


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Route: "/hbnb"

    Displays the message "HBNB" when accessed.

    Returns:
        str: The message "HBNB".
    """
    return 'HBNB'


@app.route("/c/<text>", strict_slashes=False)
def message_c(text: str):
    """
    Route: "/c/<text>"

    Displays the message "C " followed by the value of the 'text'
    variable (underscore '_' symbols replaced with a space).

    Args:
        text (str): The text parameter from the URL.

    Returns:
        str: The message "C " followed by the processed text.
    """
    t = text.replace('_', ' ')
    return 'C ' + t


@app.route("/python/<text>", strict_slashes=False)
@app.route('/python/', strict_slashes=False)
def message_python(text='is cool'):
    """
    Route: "/python/<text>"
    Route: "/python/"

    Displays the message "Python " followed by the value of the 'text'
    variable (underscore '_' symbols replaced with a space).
    The default value of 'text' is "is cool".

    Args:
        text (str, optional): The text parameter from the URL.
        Defaults to 'is cool'.

    Returns:
        str: The message "Python " followed by the processed text.
    """
    t = text.replace('_', ' ')
    return 'Python ' + t


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
