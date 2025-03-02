from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = None


def init_db(app: Flask):
    global db
    db = SQLAlchemy(app)
