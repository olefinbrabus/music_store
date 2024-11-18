from database import db
from models import Category, Instrument
from models import User


def create_category(name):
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category

def create_instrument(name, price, category_id):
    instrument = Instrument(name=name, price=price, category_id=category_id)
    db.session.add(instrument)
    db.session.commit()
    return instrument

def get_instrument_by_id(instrument_id):
    return Instrument.query.get(instrument_id)

def get_all_instruments():
    return Instrument.query.all()

def update_instrument(instrument_id, name=None, price=None, category_id=None):
    instrument = Instrument.query.get(instrument_id)
    if instrument:
        if name:
            instrument.name = name
        if price:
            instrument.price = price
        if category_id:
            instrument.category_id = category_id
        db.session.commit()
    return instrument

def delete_instrument(instrument_id):
    instrument = Instrument.query.get(instrument_id)
    if instrument:
        db.session.delete(instrument)
        db.session.commit()
    return instrument

def delete_category_with_cascade(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
    return category


def create_user(username, password):
    if User.query.filter_by(username=username).first():
        return None
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()