from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Visited_Park, Rec_Area, Activity, Park_Activity, connect_to_db, db
import os
import uuid
import hashlib
import datetime

app = Flask(__name__)

appkey = os.environ['appkey']

app.secret_key = appkey

# Raise an error in Jinja2 if an undefined variable is used.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_index():
    """Show homepage."""

    return render_template('index.html')


#############################################################################
# SIGNUP


@app.route('/signup')
def show_signup():
    """Show sign-up form."""

    return render_template('signup.html')


@app.route('/process-signup', methods=["POST"])
def process_signup():
    """Process sign-up form. Check if user in database, add if not."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    zipcode = request.form.get('zipcode')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = hash_password(password)

    reg_date = datetime.datetime.now()

    account = User.query.filter_by(email=email).first()

    if account is None:
        new_user = User(reg_date=reg_date, email=email, password=hashed_password, first_name=first_name, last_name=last_name, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()
        flash("You created an account. Please login.")
    else:
        flash("You already have an account. Please login")
    return redirect('/login')


#############################################################################
# LOGIN


@app.route('/login')
def show_login():
    """Show login page."""

    if 'user' in session:
        flash('You are already logged in')

    return render_template('login.html')


@app.route('/process-login', methods=["POST"])
def process_login():
    """Process login form. Check to see if email and password combination exist in database."""

    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = hash_password(password)

    account = User.query.filter_by(email=email).first()
    user_id = account.user_id
    first_name = account.first_name

    if check_password(hashed_password, account.password):
        flash('Welcome back, '+first_name+'!')
        session['user'] = user_id
        return render_template('')
    else:
        flash('That email and password combination does not exist.')
        return redirect('/login')


#############################################################################
# ACCOUNT/USER INFORMATION


@app.route('/account')
def show_user_account():
    pass


#############################################################################
# SEARCH


#############################################################################
# ADD TO VISITED PARKS


#############################################################################
# SHOW VISITED PARKS


#############################################################################
# LOGOUT


@app.route('/logout')
def process_logout():
    """Remove user from session"""

    if 'user' in session:
        session.pop('user', None)
        flash('You have successfully logged out.')
    else:
        flash('You are not logged in.')

    return render_template('homepage.html')


#############################################################################
# HASH FUNCTIONS


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


#############################################################################
# HELPER FUNCTIONS


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
