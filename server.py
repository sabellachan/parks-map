from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Visited_Park, Rec_Area, Activity, Park_Activity, connect_to_db, db
import os
import uuid
import hashlib
import datetime

app = Flask(__name__)

appkey = os.environ['appkey']
mapkey = os.environ['mapkey']

app.secret_key = appkey

# Raise an error in Jinja2 if an undefined variable is used.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_index():
    """Show homepage."""

    return render_template('index.html')


#############################################################################
# SIGNUP


@app.route('/signup', methods=["POST"])
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


@app.route('/login', methods=["POST"])
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

    account = User.query.filter_by(email=email).first()

    if check_password(account.password, password):
        user_id = account.user_id
        first_name = account.first_name

        flash('Welcome back, '+first_name+'!')
        session['user'] = user_id
        return render_template('landing.html', mapkey=mapkey)
    else:
        flash('That email and password combination does not exist.')
        return redirect('/login')


#############################################################################
# NICE TO HAVE: FORGOT PASSWORD


#############################################################################
# ACCOUNT/USER INFORMATION - PHASE 2


@app.route('/account')
def show_user_account():
    """Display user's account information."""

    pass
    # if 'user' in session:
    #     logged_user = session.get('user')
    #     print logged_user

    # # user = User.query.get(logged_user.user_id)
    # else:
    #     flash('You are not logged in.')
    #     return redirect('/login')

    # return render_template('account.html', user=logged_user)


# @app.route('/update-account')
# def update_user_account():
#     pass


#############################################################################
# SEARCH


@app.route('/parks.json')
def park_info():
    """JSON information about each park."""

    parks = Rec_Area.query.all()

    list_of_parks = []

    for park in parks:

        park = {'recAreaID': park.rec_area_id,
                'recAreaName': park.rec_area_name,
                'recAreaDescription': park.description,
                'recAreaLat': park.latitude,
                'recAreaLong': park.longitude,
                'recAreaPhoneNumber': park.contact_phone}

        list_of_parks.append(park)

    park_dict = {'parks': list_of_parks}

    return jsonify(park_dict)


# @app.route('/search-parks.json')
# def search_park_info():
#     """Route for search bar. PHASE 2"""
#     pass


#############################################################################
# ADD VISITED PARKS


@app.route('/add-park', methods=["POST"])
def add_visited_parks():
    """Add park to Visited_Park table for session user."""

    if 'user' in session:
        rec_area_id = request.form.get('park-name')
        user_id = session['user']

        visited = Visited_Park(rec_area_id=rec_area_id, user_id=user_id)

        # visited_parks = Visited_Park.query.filter_by(user_id=user_id, rec_area_id=rec_area_id).all()

        # if visited_parks is None:

        db.session.add(visited)
        db.session.commit()
        flash('Park successfully added.')

        # else:
        #     visited = Visited_Park(rec_area_id=rec_area_id, user_id=user_id)
        #     db.session.expunge(visited)
        #     db.session.commit()
        #     flash('Park successfully removed.')

        return render_template('landing.html', mapkey=mapkey)

    # else:
    #     flash('You are not logged in.')

    #     return render_template('index.html')


#############################################################################
# VIEW VISITED PARKS


@app.route('/view-park')
def view_visited_parks():
    pass


#############################################################################
# LOGOUT


@app.route('/logout', methods=["POST"])
def process_logout():
    """Remove user from session"""

    if 'user' in session:
        session.pop('user', None)
        flash('You have successfully logged out.')
    else:
        flash('You are not logged in.')

    return render_template('index.html')


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
