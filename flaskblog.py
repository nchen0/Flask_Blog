from flask import Flask
# creating an app variable, setting this as an instance of this flask. __name__ is just the name of the module. __name__ = __main__
app = Flask(__name__)


# This is how you create a route in the simplest form. We create routes using decorators in flask.
# / is the home page of our website. Normally we want to return HTML, but we'll start with just hello world.
@app.route("/")
@app.route("/home")
def home():
    return "<h1>Home Page!</h1>"


# To run:
"""
- set FLASK_APP=flaskblog.py
- flask run

To turn on auto update (and not have to restart the server each time):
- set FLASK_DEBUG=1
- flask run

Another way:
- if __name__ == "__main__":
    app.run(debug=True)
- python flaskblog.py
"""


@app.route("/about")
def about():
    return "<h1>About Page</h1>"

# If we ever want multiple routes handled by the same function, it's as simple as adding another decorator.
# like /home.



# Name IS main if we run this module directly with python. It is not the case if we import this module.
if __name__ == "__main__":
    app.run(debug=True)
