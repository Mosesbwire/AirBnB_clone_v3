#!/usr/bin/python3

"""
    module api/v1/views/__init__.py
    initializes the blueprint for the application
    register routes for app_views

"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
