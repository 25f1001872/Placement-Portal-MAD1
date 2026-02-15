import os

class Config:
    SECRET_KEY = "supersecretkey"
    Base_directory = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Base_directory,"..","instance","placement.db")