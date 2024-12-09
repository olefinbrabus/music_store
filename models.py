from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Index

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    instruments = relationship('Instrument', back_populates='category', cascade='all, delete-orphan')

class Instrument(db.Model):
    __tablename__ = 'instruments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    category = relationship('Category', back_populates='instruments')

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

Index('ix_instrument_category_price', Instrument.category_id, Instrument.price)