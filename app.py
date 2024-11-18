from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt
)
from config import Config
from database import db, migrate
import crud

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
jwt = JWTManager(app)

revoked_tokens = set()

# Перевірка, чи токен відкликаний
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in revoked_tokens

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = crud.create_user(username, password)
    if user is None:
        return jsonify({"error": "User already exists"}), 400

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = crud.get_user_by_username(username)
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)
    return jsonify({"message": "Token revoked"}), 200

@app.route('/categories', methods=['POST'])
@jwt_required()
def add_category():
    data = request.get_json()
    category = crud.create_category(data['name'])
    return jsonify({"id": category.id, "name": category.name})

@app.route('/instruments', methods=['POST'])
@jwt_required()
def add_instrument():
    data = request.get_json()
    instrument = crud.create_instrument(data['name'], data['price'], data['category_id'])
    return jsonify({"id": instrument.id, "name": instrument.name, "price": instrument.price, "category_id": instrument.category_id})

@app.route('/instruments/<int:instrument_id>', methods=['GET'])
@jwt_required()
def get_instrument(instrument_id):
    instrument = crud.get_instrument_by_id(instrument_id)
    if instrument:
        return jsonify({"id": instrument.id, "name": instrument.name, "price": instrument.price, "category_id": instrument.category_id})
    return jsonify({"error": "Instrument not found"}), 404

@app.route('/instruments', methods=['GET'])
@jwt_required()
def get_all_instruments():
    instruments = crud.get_all_instruments()
    return jsonify([{"id": inst.id, "name": inst.name, "price": inst.price, "category_id": inst.category_id} for inst in instruments])

@app.route('/instruments/<int:instrument_id>', methods=['PUT'])
@jwt_required()
def update_instrument(instrument_id):
    data = request.get_json()
    instrument = crud.update_instrument(instrument_id, data.get('name'), data.get('price'), data.get('category_id'))
    if instrument:
        return jsonify({"id": instrument.id, "name": instrument.name, "price": instrument.price, "category_id": instrument.category_id})
    return jsonify({"error": "Instrument not found"}), 404

@app.route('/instruments/<int:instrument_id>', methods=['DELETE'])
@jwt_required()
def delete_instrument(instrument_id):
    instrument = crud.delete_instrument(instrument_id)
    if instrument:
        return jsonify({"message": "Instrument deleted"})
    return jsonify({"error": "Instrument not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)