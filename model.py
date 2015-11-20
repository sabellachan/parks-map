"""Creates database model for national parks project"""

from flask_sqlalchemy import SQLAlchemy
import csv
import datetime
import uuid
import hashlib

db = SQLAlchemy()


class User(db.Model):
    """User of parks website."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    reg_date = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)

    parks_visited = db.relationship("Rec_Area", secondary="visited_parks", backref="users")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<User user_id={} email={} first_name={} last_name={}>'.format(self.user_id,
                                                                              self.email,
                                                                              self.first_name,
                                                                              self.last_name)


class Visited_Park(db.Model):
    """Parks visited by users."""

    __tablename__ = 'visited_parks'

    visited_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rec_area_id = db.Column(db.Integer, db.ForeignKey('rec_areas.rec_area_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def add_to_db(self):
        """Check to see if user has visited this park before."""

        if_visited = Visited_Park.query.filter(Visited_Park.user_id == self.user_id, Visited_Park.rec_area_id == self.rec_area_id).all()
        # check to see if user has not visited this park
        # if user has not added this park, add it to the database
        if len(if_visited) == 0:
            db.session.add(self)
            db.session.commit()
            return "Park Added"
        # if user has already added this park, remove it from database
        else:
            visited = db.session.query(Visited_Park).filter(Visited_Park.user_id == self.user_id, Visited_Park.rec_area_id == self.rec_area_id).first()
            db.session.delete(visited)
            db.session.commit()
            return "Park Removed"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Visited Parks visited_id={} rec_area_id={} user_id={}>'.format(self.visited_id,
                                                                                self.rec_area_id,
                                                                                self.user_id)


class Rec_Area(db.Model):
    """Information about recreation areas."""

    __tablename__ = 'rec_areas'

    rec_area_id = db.Column(db.Integer, nullable=False, primary_key=True)
    rec_area_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    location = db.Column(db.Text, nullable=True)
    contact_phone = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Rec_Areas rec_area_id={} rec_area_name={}>'.format(self.rec_area_id,
                                                                    self.rec_area_name)


class Activity(db.Model):
    """Activities available throughout the whole parks system."""

    __tablename__ = 'activities'

    activity_id = db.Column(db.Integer, nullable=False, primary_key=True)
    activity_name = db.Column(db.String(30), nullable=False)

    rec_areas = db.relationship("Rec_Area", secondary="park_activities", backref="activities")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Activities activity_id={} activity_name={}>'.format(self.activity_id,
                                                                     self.activity_name)


class Park_Activity(db.Model):
    """Activities available within certain parks."""

    __tablename__ = 'park_activities'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), nullable=False)
    rec_area_id = db.Column(db.Integer, db.ForeignKey('rec_areas.rec_area_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Park_Activities id={} activity_id={} rec_area_id={}>'.format(self.id,
                                                                              self.activity_id,
                                                                              self.rec_area_id)

#############################################################################
# ADD EXAMPLE DATA FOR TESTING


def example_data_rec_areas():
    """Create some sample rec area data."""

    # If tests are run more than once, empty out existing data
    Rec_Area.query.delete()

    # Add sample rec areas
    rec_areas = open('seed_data/rec_areas_test.csv')

    data = csv.reader(rec_areas)

    for row in data:
        description, rec_area_id, latitude, longitude, rec_area_name, contact_phone, location = row

        rec_area = Rec_Area(rec_area_id=rec_area_id,
                            rec_area_name=rec_area_name,
                            description=description,
                            latitude=latitude,
                            longitude=longitude,
                            location=location,
                            contact_phone=contact_phone)

        db.session.add(rec_area)

    db.session.commit()


def example_data_users():
    """Create some sample user data."""

    # If tests are run more than once, empty out existing data
    User.query.delete()

    reg_date = datetime.datetime.now()

    maynard = User(user_id=1, reg_date=reg_date, email='admin@maynard.com', password=hash_password('wackywoo'), first_name='Maynard', last_name='Burns', zipcode='94107')
    lucy = User(user_id=2, reg_date=reg_date, email='lucy@test.com', password=hash_password('brindlepuppy'), first_name='Lucy', last_name='Vo', zipcode='94587')
    flynn = User(user_id=3, reg_date=reg_date, email='flynn@ryder.com', password=hash_password('rapunzel'), first_name='Flynn', last_name='Ryder', zipcode='10001')
    alice = User(user_id=4, reg_date=reg_date, email='alice@thelookingglass.com', password=hash_password('whiterabbit'), first_name='Alice', last_name='Wonderland', zipcode='64850')

    db.session.add_all([maynard, lucy, flynn, alice])
    db.session.commit()


def example_data_visits():
    """Create some sample visit data."""

    # If tests are run more than once, empty out existing data
    Visited_Park.query.delete()

    # User 01's visits
    visit0101 = Visited_Park(visited_id=1, rec_area_id=2647, user_id=1)
    visit0102 = Visited_Park(visited_id=2, rec_area_id=2991, user_id=1)
    visit0103 = Visited_Park(visited_id=3, rec_area_id=2988, user_id=1)
    visit0104 = Visited_Park(visited_id=4, rec_area_id=2994, user_id=1)

    # User 02's visits
    visit0201 = Visited_Park(visited_id=5, rec_area_id=2647, user_id=2)
    visit0202 = Visited_Park(visited_id=6, rec_area_id=2991, user_id=2)
    visit0203 = Visited_Park(visited_id=7, rec_area_id=2988, user_id=2)
    visit0204 = Visited_Park(visited_id=8, rec_area_id=2733, user_id=2)

    # User 03's visits
    visit0301 = Visited_Park(visited_id=9, rec_area_id=2941, user_id=3)
    visit0302 = Visited_Park(visited_id=10, rec_area_id=2991, user_id=3)
    visit0303 = Visited_Park(visited_id=11, rec_area_id=2994, user_id=3)
    visit0304 = Visited_Park(visited_id=12, rec_area_id=2725, user_id=3)

    # User 04's visits
    visit0401 = Visited_Park(visited_id=13, rec_area_id=2647, user_id=4)
    visit0402 = Visited_Park(visited_id=14, rec_area_id=2988, user_id=4)
    visit0403 = Visited_Park(visited_id=15, rec_area_id=2733, user_id=4)
    visit0404 = Visited_Park(visited_id=16, rec_area_id=2725, user_id=4)

    db.session.add_all([visit0101, visit0102, visit0103, visit0104,
                        visit0201, visit0202, visit0203, visit0204,
                        visit0301, visit0302, visit0303, visit0304,
                        visit0401, visit0402, visit0403, visit0404])
    db.session.commit()


#############################################################################
# HASH FUNCTION


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


##############################################################################
# Connect to database


def connect_to_db(app, db_uri='sqlite:///parks.db'):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Allows interactive querying in the shell.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
