#!/usr/bin/python3

"""
6-number_odd_or_even.py

This script defines a Flask web application with seven routes, including
a route that renders an HTML template based on whether a number is odd or even.

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
- "/number/<int:n>": Displays the message "<n> is a number" if 'n' is
  an integer.
- "/number_template/<int:n>": Renders an HTML template ("5-number.html")
  with the 'number' parameter.
- "/number_odd_or_even/<int:n>": Renders an HTML template
  ("6-number_odd_or_even.html") with the 'n' parameter and a message
  indicating whether the number is odd or even.
"""

from flask import Flask, render_template

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

    Displays the message "Python " followed by the value of the 'text' variable
    (underscore '_' symbols replaced with a space).
    The default value of 'text' is "is cool".

    Args:
        text (str, optional): The text parameter from the URL.
        Defaults to 'is cool'.

    Returns:
        str: The message "Python " followed by the processed text.
    """
    t = text.replace('_', ' ')
    return 'Python ' + t


@app.route("/number/<int:n>", strict_slashes=False)
def message_number(n: int):
    """
    Route: "/number/<int:n>"

    Displays the message "<n> is a number" if 'n' is an integer.

    Args:
        n (int): The integer parameter from the URL.

    Returns:
        str: The message "<n> is a number".
    """
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n: int):
    """
    Route: "/number_template/<int:n>"

    Renders an HTML template ("5-number.html") with the 'number' parameter.

    Args:
        n (int): The integer parameter from the URL.

    Returns:
        str: Rendered HTML template.
    """
    return render_template("5-number.html", number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_template_odd(n: int):
    """
    Route: "/number_odd_or_even/<int:n>"

    Renders an HTML template ("6-number_odd_or_even.html") with the 'n'
    parameter and a message indicating whether the number is odd or even.

    Args:
        n (int): The integer parameter from the URL.

    Returns:
        str: Rendered HTML template.
    """
    b = 'odd' if n % 2 != 0 else 'even'
    return render_template("6-number_odd_or_even.html", n=n, b=b)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
