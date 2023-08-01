#!/usr/bin/python3
""" create a new view for City objects """


from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/api/v1/states/<string:state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """ retieves City object by state id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app.route('/api/v1/cities/<string:city_id>', methods=['GET'])
def get_city(city_id):
    """ retrieves City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app.route('/api/v1/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ deletes a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app.route('/api/v1/states/<string:state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ creates a City object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    city = City(**data)
    city.state_id = state_id()
    city.save()
    return jsonify(city.to_dict()), 201


@app.route('/api/v1/cities/<string:city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200


if __name__ == "__main__":
    """ main function """
    app.run(host="0.0.0.0", port=5000)
