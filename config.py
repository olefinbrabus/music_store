import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///music_store.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False