#!/usr/bin/python3
"""Index file"""
from flask import jsonify
from models.__init__ import storage
from models import amenity as Amenity
from models import city as City
from models import place as Place
from models import state as State
from models import review as Review
from models import user as User

from api.v1.views.__init__ import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """returns status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns statistics"""

    data = {
        "amenities": len(storage.all('Amenity')),
        "cities": len(storage.all('City')),
        "places": len(storage.all('Place')),
        "reviews": len(storage.all('Review')),
        "states": len(storage.all('State')),
        "users": len(storage.all('User'))
    }
    return jsonify(data)
