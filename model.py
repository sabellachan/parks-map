"""Creates database model for national parks project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User of parks website."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    reg_date = db.Column(db.Timestamp, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)

    visit = db.relationship('Visited_Parks', backref=db.backref('users', order_by=user_id))

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
    entity_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('Users', backref=db.backref('visited_parks', order_by=visited_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Visited Parks visited_id={} entity_id={} user_id={}>'.format(self.visited_id,
                                                                              self.entity_id,
                                                                              self.user_id)


class Rec_Area(db.Model):
    """Information about recreation areas."""

    __tablename__ = 'rec_areas'

    recarea_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entity_id = db.Column(db.Integer, nullable=False)
    entity_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    contact_phone = db.Column(db.String(15), nullable=True)
    reservation_url = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Rec_Areas recarea_id={} entity_id={} entity_name={}>'.format(self.recarea_id,
                                                                              self.entity_id,
                                                                              self.entity_name)


class Activity(db.Model):
    """Activities available throughout the whole parks system."""

    __tablename__ = 'activities'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_id = db.Column(db.Integer, nullable=False)
    activity_name = db.Column(db.String(30), nullable=False)

    park_activity = db.relationship('Park_Activities', backref=db.backref('activities', order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Activities id={} activity_id={} activity_name={}>'.format(self.id,
                                                                           self.activity_id,
                                                                           self.activity_name)


class Park_Activity(db.Model):
    """Activities available within certain parks."""

    __tablename__ = 'park_activities'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_id = db.Column(db.Integer, nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)

    activity = db.relationship('Activities', backref=db.backref('park_activities', order_by=id))

    entity = db.relationship('Rec_Areas', backref=db.backref('park_activities', order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Park_Activities id={} activity_id={} entity_id={}>'.format(self.id,
                                                                            self.activity_id,
                                                                            self.entity_id)


class Organization(db.Model):
    """Organizations in charge of recreation areas."""

    __tablename__ = 'organizations'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    org_id = db.Column(db.Integer, nullable=False)
    org_name = db.Column(db.String(40), nullable=False)
    org_jurisdication = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Organizations id={} org_id={} org_name={} org_jurisdication={}>'.format(self.id,
                                                                                         self.org_id,
                                                                                         self.org_name,
                                                                                         self.org_jurisdication)


class Park_Org(db.Model):
    """Organizations that specific parks are governed by."""

    __tablename__ = 'park_orgs'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    org_id = db.Column(db.Integer, nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)

    organization = db.relationship('Organizations', backref=db.backref('park_orgs', order_by=id))

    entity = db.relationship('Rec_Areas', backref=db.backref('park_orgs', order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Park_Orgs id={} org_id={} entity_id={}>'.format(self.id, self.org_id, self.entity_id)


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
