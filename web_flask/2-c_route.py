"""
2-c_route.py

This script defines a Flask web application with three routes.

Usage:
- Run the script, and the web application will be accessible at
  http://0.0.0.0:5000.

Routes:
- "/": Displays the message "Hello HBNB!" when accessed.
- "/hbnb": Displays the message "HBNB" when accessed.
- "/c/<text>": Displays the message "C " followed by the value of the
  'text' variable (underscore '_' symbols replaced with a space).

Author: [Your Name]
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
def message(text: str):
    """
    Route: "/c/<text>"

    Displays the message "C " followed by the value of the 'text' variable
    (underscore '_' symbols replaced with a space).

    Args:
        text (str): The text parameter from the URL.

    Returns:
        str: The message "C " followed by the processed text.
    """
    t = text.replace('_', ' ')
    return 'C ' + t


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
