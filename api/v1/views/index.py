#!/usr/bin/python3
"""
    module api/v1/views/index.py:
    holds routes for app_views blueprint
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """ route:GET
    returns JSON response indicating api is up
    """

    return jsonify({
        'status': 'OK'
    })
