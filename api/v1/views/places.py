#!/usr/bin/python3
"""Places file"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views.__init__ import app_views


class_name = "Place"


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def city_places(city_id):
    """returns Places for a City"""
    data = []

    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    all_data = storage.all(class_name)
    for k, v in all_data.items():
        if v.city_id == city_id:
            data.append(v.to_dict())

    return jsonify(data)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=["GET"])
def get_specific_place(place_id):
    """returns specified Place"""
    data = {}

    v = storage.get(class_name, place_id)
    if v is None:
        abort(404)

    data = v.to_dict()

    return data


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_specific_place(place_id):
    """returns specified Place"""
    v = storage.get(class_name, place_id)
    if v is None:
        abort(404)

    storage.delete(v)
    storage.save()

    return {}, 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=["POST"])
def post_new_place(city_id):
    """saves new Place"""
    from models.place import Place

    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)

    if 'name' not in data:
        abort(400, "Missing name")

    attribs = {
        "name": data['name'],
        "city_id": city_id,
        "user_id": data['user_id']
    }

    new_place = Place(**attribs)
    storage.save()

    return new_place.to_dict(), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=["PUT"])
def put_specific_place(place_id):
    """returns updated Place"""

    existing = storage.get(class_name, place_id)
    if existing is None:
        abort(404)

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()

    for k, v in data.items():
        setattr(existing, k, v)

    storage.save()
    storage.reload()

    updated = storage.get(class_name, place_id)
    if updated is None:
        abort(404)

    return updated.to_dict(), 200
