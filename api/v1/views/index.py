#!/usr/bin/python3
"""Index file"""
from flask import jsonify

from api.v1.views.__init__ import app_views

@app_views.route('/status', strict_slashes=False)
def status():
    """returns status ok"""
    return jsonify({"status":"OK"})
