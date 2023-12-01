#!/usr/bin/python3
"""
starts a Flask web application
"""

from models import storage
from os import getenv
from api.v1.views.__init__ import app_views
from flask import Flask, Blueprint
app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    if host is None:
        host = '0.0.0.0'

    if port is None:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
