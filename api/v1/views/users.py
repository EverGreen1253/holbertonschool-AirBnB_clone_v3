#!/usr/bin/python3
"""Users file"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views.__init__ import app_views


class_name = "User"


@app_views.route('/users', strict_slashes=False)
def users():
    """returns Users"""
    data = []

    all_data = storage.all(class_name)
    for k, v in all_data.items():
        # name = k.split(".")[0]

        data.append({
            "__class__": class_name,
            "id": v.id,
            "first_name": v.first_name,
            "last_name": v.last_name,
            "email": v.email,
            "password": v.password,
            "created_at": v.created_at,
            "updated_at": v.updated_at
        })

    return jsonify(data)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=["GET"])
def get_specific_user(user_id):
    """returns specified User"""
    data = {}

    v = storage.get(class_name, user_id)
    if v is None:
        abort(404)

    data = {
        "__class__": class_name,
        "id": v.id,
        "first_name": v.first_name,
        "last_name": v.last_name,
        "email": v.email,
        "password": v.password,
        "created_at": v.created_at,
        "updated_at": v.updated_at
    }

    return data


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_specific_user(user_id):
    """returns specified User"""
    v = storage.get(class_name, user_id)
    if v is None:
        abort(404)

    storage.delete(v)
    storage.save()

    return {}, 200


@app_views.route('/users', strict_slashes=False,
                 methods=["POST"])
def post_specific_user():
    """saves specified User"""
    from models.user import User

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")

    attribs = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "password": data["password"]
    }

    new_user = User(**attribs)
    storage.save()

    return new_user.to_dict(), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=["PUT"])
def put_specific_user(user_id):
    """returns updated User"""

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400)

    existing = storage.get(class_name, user_id)
    if existing is None:
        abort(404)

    for k, v in data.items():
        setattr(existing, k, v)

    storage.save()
    storage.reload()

    updated = storage.get(class_name, user_id)
    if updated is None:
        abort(404)

    return updated.to_dict(), 200
