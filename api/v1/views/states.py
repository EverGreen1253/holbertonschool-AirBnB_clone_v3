#!/usr/bin/python3
"""States file"""
from flask import jsonify, abort, request
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


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["GET"])
def get_specific_state(state_id):
    """returns specified State"""
    data = {}

    v = storage.get(class_name, state_id)
    if v is None:
        abort(404)

    data = {
        "__class__": class_name,
        "created_at": v.created_at,
        "id": v.id,
        "name": v.name,
        "updated_at": v.updated_at
    }

    return data


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["DELETE"])
def del_specific_state(state_id):
    """returns specified State"""
    v = storage.get(class_name, state_id)
    if v is None:
        abort(404)

    storage.delete(v)
    storage.save()

    return {}, 200


@app_views.route('/states', strict_slashes=False, methods=["POST"])
def post_specific_state():
    """returns specified State"""
    from models.state import State
    # from datetime import datetime
    # import uuid

    if request.get_json() is None:
        abort(400)

    data = request.get_json()
    if 'name' not in data:
        abort(400)

    # now = datetime.utcnow()

    attribs = {
        # "__class__": class_name,
        # "id": str(uuid.uuid4()),
        "name": data['name'],
        # "created_at": now,
        # "updated_at": now
    }

    new_state = State(**attribs)
    storage.save()

    return new_state.to_dict(), 201
