import os
from dotenv import dotenv_values

env_dict = dotenv_values()

class Config:
    SQLALCHEMY_DATABASE_URI = env_dict["GOOGLE_CLOUD_CONNECTION_POSTGRES"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecretkey')