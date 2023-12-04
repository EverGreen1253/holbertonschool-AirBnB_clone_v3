#!/usr/bin/python3
"""States file"""
from flask import jsonify
from models import storage
from api.v1.views.__init__ import app_views

class_name = "State"

@app_views.route('/states', strict_slashes=False)
def states():
    """returns States"""
    data = []

    all_data = storage.all(class_name)
    for k, v in all_data.items():
        # name = k.split(".")[0]

        data.append({
            "__class__": class_name,
            "created_at": v.created_at,
            "id": v.id,
            "name": v.name,
            "updated_at": v.updated_at
        })

    return jsonify(data)


@app_views.route('/states/<state_id>', strict_slashes=False)
def state_specific(state_id):
    """returns specified State"""
    data = {}

    v = storage.get(class_name, state_id)
    data = {
        "__class__": class_name,
        "created_at": v.created_at,
        "id": v.id,
        "name": v.name,
        "updated_at": v.updated_at
    }

    return data
