#!/usr/bin/python3

"""
    module api/v1/app.py
    creates Flask app and register blueprint app_views
    the flask application entry point
"""

from os import getenv
from flask import Flask
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def closeConnection(exception):
    """ terminates connection to storage """
    storage.close()


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
