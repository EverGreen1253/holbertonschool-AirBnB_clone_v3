#!/usr/bin/python3
"""Index file"""
from flask import jsonify
from models.__init__ import storage
from api.v1.views.__init__ import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """returns status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns statistics"""

    data = {
        "amenities": 0,
        "cities": 0,
        "places": 0,
        "reviews": 0,
        "states": 0,
        "users": 0
    }

    # call storage.all() just one time to minimise
    # number of db connections
    all = storage.all()
    for k, v in all.items():
        name = k.split(".")[0]

        if name == 'Amenity':
            data['amenities'] = data['amenities'] + 1
        elif name == 'City':
            data['cities'] = data['cities'] + 1
        elif name == 'Place':
            data['places'] = data['places'] + 1
        elif name == 'Review':
            data['reviews'] = data['reviews'] + 1
        elif name == 'State':
            data['states'] = data['states'] + 1
        elif name == 'User':
            data['users'] = data['users'] + 1

    return jsonify(data)
