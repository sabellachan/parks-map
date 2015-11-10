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


@app.route('/login', methods=["GET", "POST"])
def show_login():
    """Show login page."""

    if 'user' in session:
        flash('You are already logged in')

    return render_template('login.html')


@app.route('/process-login', methods=["GET", "POST"])
def process_login():
    """Process login form. Check to see if email and password combination exist in database."""

    email = request.form.get('email')
    password = request.form.get('password')

    try:
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

    except AttributeError:
        flash('Please enter a valid email or password.')
        return redirect('/login')


@app.route('/landing')
def show_landing_page():
    """Show landing page from links other than login."""

    return render_template('landing.html', mapkey=mapkey)


#############################################################################
# NICE TO HAVE: FORGOT PASSWORD


#############################################################################
# ACCOUNT/USER INFORMATION


@app.route('/account')
def show_user_account():
    """Display user's account information."""

    if 'user' in session:
        logged_user = session['user']
        user = User.query.get(logged_user)
        return render_template('account.html', user=user)

    else:
        flash('You are not logged in.')
        return redirect('/login')


# NICE TO HAVE
# @app.route('/update-account')
# def update_user_account():
#     pass


#############################################################################
# RETRIEVE PARKS INFORMATION


@app.route('/parks.json')
def park_info():
    """JSON information about each unvisited park."""

    subquery = db.session.query(Visited_Park.rec_area_id)
    parks = db.session.query(Rec_Area).filter(Rec_Area.rec_area_id.notin_(subquery)).all()

    list_of_parks = []

    for park in parks:

        activities_query = db.session.query(Activity.activity_name).join(Park_Activity).filter(Park_Activity.rec_area_id == str(park.rec_area_id))
        list_of_activities = activities_query.all()

        park = {'recAreaID': park.rec_area_id,
                'recAreaName': park.rec_area_name,
                'recAreaDescription': park.description,
                'recAreaActivities': list_of_activities,
                'recAreaLat': park.latitude,
                'recAreaLong': park.longitude,
                'recAreaPhoneNumber': park.contact_phone}

        list_of_parks.append(park)

    park_dict = {'parks': list_of_parks}

    return jsonify(park_dict)


@app.route('/parks-visited.json')
def visited_park_info():
    """JSON information about each visited park."""

    user_id = session['user']

    visited_parks = db.session.query(Rec_Area).join(Visited_Park).filter(Visited_Park.user_id == user_id).all()

    list_of_visited = []

    for visited_park in visited_parks:

        activities_query = db.session.query(Activity.activity_name).join(Park_Activity).filter(Park_Activity.rec_area_id == str(visited_park.rec_area_id))
        list_of_activities = activities_query.all()

        visited_park = {'recAreaID': visited_park.rec_area_id,
                        'recAreaName': visited_park.rec_area_name,
                        'recAreaDescription': visited_park.description,
                        'recAreaActivities': list_of_activities,
                        'recAreaLat': visited_park.latitude,
                        'recAreaLong': visited_park.longitude,
                        'recAreaPhoneNumber': visited_park.contact_phone}

        list_of_visited.append(visited_park)

    visited_dict = {'parks': list_of_visited}

    return jsonify(visited_dict)


#############################################################################
# ADD VISITED PARKS


@app.route('/add-park', methods=["POST"])
def add_visited_parks():
    """Add park to Visited_Park table for session user."""

    if 'user' in session:
        rec_area_id = request.form.get('park-id')
        user_id = session['user']

        visited = Visited_Park(rec_area_id=rec_area_id, user_id=user_id)

        message = visited.add_to_db()

    else:
        flash('You are not logged in.')
        return render_template('index.html')

    return message


#############################################################################
# VIEW VISITED PARKS


@app.route('/view-park')
def view_visited_parks():
    """Show parks user has visited."""

    if 'user' in session:
        user_id = session['user']
        # visited_parks is a list
        visited_parks = db.session.query(Rec_Area).join(Visited_Park).filter(Visited_Park.user_id == user_id).all()

        return render_template('visited.html', parks=visited_parks)
    else:
        flash('You are not logged in.')
        return render_template('index.html')


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
