"""Creates database model for national parks project"""

from flask_sqlalchemy import SQLAlchemy

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
    contact_phone = db.Column(db.String(15), nullable=True)
    reservation_url = db.Column(db.String(60), nullable=True)

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


##############################################################################
# Connect to database

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parks.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Allows interactive querying in the shell.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
