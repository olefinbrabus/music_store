# app.py
from flask import Flask, jsonify, request
from config import Config
from database import db, migrate
from models import Category, Instrument
import crud

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

@app.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    category = crud.create_category(data['name'])
    return jsonify({"id": category.id, "name": category.name})

@app.route('/instruments', methods=['POST'])
def add_instrument():
    data = request.get_json()
    instrument = crud.create_instrument(data['name'], data['price'], data['category_id'])
    return jsonify({"id": instrument.id, "name": instrument.name, "price": instrument.price, "category_id": instrument.category_id})

@app.route('/instruments/<int:instrument_id>', methods=['GET'])
def get_instrument(instrument_id):
    instrument = crud.get_instrument_by_id(instrument_id)
    if instrument:
        return jsonify({"id": instrument.id, "name": instrument.name, "price": instrument.price, "category_id": instrument.category_id})
    return jsonify({"error": "Instrument not found"}), 404

@app.route('/instruments', methods=['GET'])
def get_all_instruments():
    instruments = crud.get_all_instruments()
    return jsonify([{"id": inst.id, "name": inst.name, "price": inst.price, "category_id": inst.category_id} for inst in instruments])

@app.route('/instruments/<int:instrument_id>', methods=['PUT'])
def update_instrument(instrument_id):
    data = request.get_json()
    instrument = crud.update_instrument(instrument_id, data.get('name'), data.get('price'), data.get('category_id'))
    if instrument:
        return jsonify({"id": instrument.id, "name": instrument.name, "price": instrument.price, "category_id": instrument.category_id})
    return jsonify({"error": "Instrument not found"}), 404

@app.route('/instruments/<int:instrument_id>', methods=['DELETE'])
def delete_instrument(instrument_id):
    instrument = crud.delete_instrument(instrument_id)
    if instrument:
        return jsonify({"message": "Instrument deleted"})
    return jsonify({"error": "Instrument not found"}), 404

@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = crud.delete_category_with_cascade(category_id)
    if category:
        return jsonify({"message": "Category and related instruments deleted"})
    return jsonify({"error": "Category not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)