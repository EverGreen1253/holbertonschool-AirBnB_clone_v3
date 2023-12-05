#!/usr/bin/python3
"""Reviews file"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views.__init__ import app_views


class_name = "Review"


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def place_reviews(place_id):
    """returns Reviews for a Place"""
    data = []

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    all_data = storage.all(class_name)
    for k, v in all_data.items():
        if v.place_id == place_id:
            data.append(v.to_dict())

    return jsonify(data)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=["GET"])
def get_specific_review(review_id):
    """returns specified Review"""
    data = {}

    v = storage.get(class_name, review_id)
    if v is None:
        abort(404)

    data = v.to_dict()

    return data


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_specific_review(review_id):
    """returns specified Review"""
    v = storage.get(class_name, review_id)
    if v is None:
        abort(404)

    storage.delete(v)
    storage.save()

    return {}, 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=["POST"])
def post_new_review(place_id):
    """saves new Place"""
    from models.place import Review

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)

    if 'text' not in data:
        abort(400, "Missing text")

    attribs = {
        "text": data['text'],
        "place_id": place_id,
        "user_id": data['user_id']
    }

    new_review = Review(**attribs)
    storage.save()

    return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=["PUT"])
def put_specific_place(review_id):
    """returns updated Review"""

    existing = storage.get(class_name, review_id)
    if existing is None:
        abort(404)

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()

    for k, v in data.items():
        setattr(existing, k, v)

    storage.save()
    storage.reload()

    updated = storage.get(class_name, review_id)
    if updated is None:
        abort(404)

    return updated.to_dict(), 200
