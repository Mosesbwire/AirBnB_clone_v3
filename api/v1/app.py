#!/usr/bin/python3
""" Entry point for the flask application """

from os import getenv
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def closeConnection(exception):
    """ terminates connection to storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handles all responses when route is not found """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def client_error(error):
    """ Handles all 400 client errors """
    
    return error.description, 400


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
