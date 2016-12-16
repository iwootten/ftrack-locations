import os
import sys


def get_old_location():

    module = os.environ.get("FTRACK_LOCATIONS_MODULE", "")
    sys.path.append(os.path.dirname(__file__))

    location = __import__(module).get_old_location()
    return location


def get_new_location():

    module = os.environ.get("FTRACK_LOCATIONS_MODULE", "")
    sys.path.append(os.path.dirname(__file__))

    location = __import__(module).get_new_location()
    return location
