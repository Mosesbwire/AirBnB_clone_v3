#!/usr/bin/python3
"""
    module api/v1/views/states.py:
    holds routes for state blueprint
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ route:GET
    returns all state objects in storage
    """
    data = storage.all('State')
    results = []
    for key, value in data.items():
        results.append(data[key].to_dict())

    return jsonify(results)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ route: GET
        get state by id
        raises 404 error if id is not linked to any object
    """
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete(state_id):
    """route: DELETE
        deletes object with associated id from storage
        raises 404 error if id is not linked to any object
    """
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)

    state.delete()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """ creates new state object and persists to storage """

    if not request.get_json():
        abort(400, "Not a json")

    if not 'name' in request.json:
        abort(400, "Missing name")

    data = request.get_json()

    state = State(**data)

    state.save()

    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ PUT /states/<state_id>
        Updates a State object
    """
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
