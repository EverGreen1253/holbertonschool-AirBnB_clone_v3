#!/usr/bin/python3
"""Amenities file"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views.__init__ import app_views


class_name = "Amenity"


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """returns Amenities"""
    data = []

    all_data = storage.all(class_name)
    for k, v in all_data.items():

        data.append({
            "__class__": class_name,
            "id": v.id,
            "name": v.name,
            "created_at": v.created_at,
            "updated_at": v.updated_at
        })

    return jsonify(data)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["GET"])
def get_specific_amenity(amenity_id):
    """returns specified Amenity"""
    data = {}

    v = storage.get(class_name, amenity_id)
    if v is None:
        abort(404)

    data = {
        "__class__": class_name,
        "id": v.id,
        "name": v.name,
        "created_at": v.created_at,
        "updated_at": v.updated_at
    }

    return data


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_specific_amenity(amenity_id):
    """returns specified Amenity"""
    v = storage.get(class_name, amenity_id)
    if v is None:
        abort(404)

    storage.delete(v)
    storage.save()

    return {}, 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=["POST"])
def post_specific_amenity():
    """saves specified Amenity"""
    from models.amenity import Amenity

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")

    attribs = {
        "name": data['name'],
    }

    new_amenity = Amenity(**attribs)
    storage.save()

    return new_amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["PUT"])
def put_specific_amenity(amenity_id):
    """returns updated Amenity"""

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400)

    existing = storage.get(class_name, amenity_id)
    if existing is None:
        abort(404)

    for k, v in data.items():
        setattr(existing, k, v)

    storage.save()
    storage.reload()

    updated = storage.get(class_name, amenity_id)
    if updated is None:
        abort(404)

    return updated.to_dict(), 200
