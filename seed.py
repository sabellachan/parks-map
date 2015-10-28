"""Utility file to make seed data into database via seed files and API calls to ridb.recreation.gov."""

import json
import urllib
import os
from model import Rec_Area, Activity, Park_Activity, connect_to_db, db

from server import app
import csv

key = os.environ['key']


def load_rec_areas():
    """Retrieve information about entities within recreation.gov and load into database. Refers to Rec_Area."""

    # if there's an existing table, delete and reload it
    Rec_Area.query.delete()

    rec_areas = open('seed_data/rec_areas.csv')

    data = csv.reader(rec_areas)

    for row in data:
    # row is a list
        description, rec_area_id, latitude, longitude, rec_area_name, contact_phone, reservation_url = row

        description.decode('utf-8')

        try:
            latitude = float(latitude)
            longitude = float(longitude)

        except ValueError:
            latitude = None
            longitude = None

        rec_area = Rec_Area(rec_area_id=rec_area_id,
                            rec_area_name=rec_area_name,
                            description=description,
                            latitude=latitude,
                            longitude=longitude,
                            contact_phone=contact_phone,
                            reservation_url=reservation_url)

        db.session.add(rec_area)

        db.session.commit()


def load_activities():
    """Retrieve activities information from recreation.gov and load into database. Refers to Activity."""

    # if there's an existing table, delete and reload it
    Activity.query.delete()

    # returns a dictionary with a list of dictionaries nested
    results = json.load(urllib.urlopen('https://ridb.recreation.gov/api/v1/activities/?apikey={}'.format(key)))

    # returns a list of dictionaries
    activities = results[u'RECDATA']

    # line is a dictionary
    for line in activities:

        activity_id = line[u'ActivityID']
        activity_name = line[u'ActivityName'].lower()

        activity = Activity(activity_id=activity_id, activity_name=activity_name)

        db.session.add(activity)

    db.session.commit()


def load_park_activities():
    """Retrieve what activities are available within what parks and load into database. Refers to Park_Activity."""

    Park_Activity.query.delete()

    for row in open('seed_data/entity_activities'):
        row = row.rstrip()
        # row.split() brings back a list of pairs
        activity_id, rec_area_id = row.split()

        park_activity = Park_Activity(activity_id=activity_id, rec_area_id=rec_area_id)

        db.session.add(park_activity)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # Create all tables if they haven't been created
    db.create_all()

    # Import different types of data
    load_rec_areas()
    load_activities()
    load_park_activities()
