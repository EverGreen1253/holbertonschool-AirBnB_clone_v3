#!/usr/bin/python3
"""
starts a Flask web application
"""

from models import storage
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    if host is None:
        host = '0.0.0.0'

    if port is None:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
