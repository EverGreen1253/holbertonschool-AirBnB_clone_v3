#!/usr/bin/python3
"""States file"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views.__init__ import app_views


class_name = "City"


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def state_cities(state_id):
    """returns Cities"""
    data = []

    all_data = storage.all(class_name)
    for k, v in all_data.items():

        if v.state_id == state_id:
            data.append({
                "__class__": class_name,
                "id": v.id,
                "name": v.name,
                "state_id": v.state_id,
                "created_at": v.created_at,
                "updated_at": v.updated_at
            })

    if len(data) == 0:
        abort(404)

    return jsonify(data)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=["GET"])
def get_specific_city(city_id):
    """returns specified City"""
    data = {}

    v = storage.get(class_name, city_id)
    if v is None:
        abort(404)

    data = {
        "__class__": class_name,
        "created_at": v.created_at,
        "id": v.id,
        "name": v.name,
        "state_id": v.state_id,
        "updated_at": v.updated_at
    }

    return data


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_specific_city(city_id):
    """returns specified City"""
    v = storage.get(class_name, city_id)
    if v is None:
        abort(404)

    storage.delete(v)
    storage.save()

    return {}, 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=["POST"])
def post_specific_city(state_id):
    """saves specified City"""
    from models.state import City

    existing = storage.get("State", state_id)
    if existing is None:
        abort(404)

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")

    attribs = {
        "name": data['name'],
        "state_id": state_id,
    }

    new_city = City(**attribs)
    storage.save()

    return new_city.to_dict(), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=["PUT"])
def put_specific_city(city_id):
    """returns updated City"""

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400)

    existing = storage.get(class_name, city_id)
    if existing is None:
        abort(404)

    for k, v in data.items():
        setattr(existing, k, v)

    storage.save()
    storage.reload()

    updated = storage.get(class_name, city_id)
    if updated is None:
        abort(404)

    return updated.to_dict(), 200
