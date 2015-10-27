from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Visited_Park, Rec_Area, Activity, Park_Activity, connect_to_db, db
import os

app = Flask(__name__)

appkey = os.environ['appkey']

app.secret_key = appkey

# Raise an error in Jinja2 if an undefined variable is used.
app.jinja_env.undefined = StrictUndefined


# add routes here
@app.route('/')
def show_index():
    pass


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
