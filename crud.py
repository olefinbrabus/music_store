from database import db
from models import Category, Instrument
from models import User
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_, or_
from sqlalchemy import func


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


def get_filtered_instruments(
        price_min: float = None,
        price_max: float = None,
        category_ids: list[int] = None,
        search: str = None
):
    query = db.query(Instrument)

    if price_min is not None:
        query = query.filter(Instrument.price >= price_min)
    if price_max is not None:
        query = query.filter(Instrument.price <= price_max)
    if category_ids:
        query = query.filter(Instrument.category_id.in_(category_ids))
    if search:
        query = query.filter(Instrument.name.ilike(f"%{search}%"))

    return query.all()


def get_sorted_instruments(
        sort_by: str = "price",
        order: str = "asc",
        limit: int = 10,
        offset: int = 0
):
    query = db.query(Instrument)
    if sort_by in ["price", "name", "created_at"]:
        column = getattr(Instrument, sort_by)
        if order == "desc":
            column = column.desc()
        query = query.order_by(column)

    return query.offset(offset).limit(limit).all()


def get_instruments_count_by_category():
    return db.query(
        Instrument.category_id,
        func.count(Instrument.id).label("instrument_count")
    ).group_by(Instrument.category_id).all()
