"""Utility file to make API calls to ridb.recreation.gov and seed database."""

import json
import urllib
import os
from model import User, Visited_Park, Rec_Area, Activity, Park_Activity, Organization, Park_Org

from model import connect_to_db, db
from server import app
import datetime

apikey = os.environ["apikey"]

