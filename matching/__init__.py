from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object(os.environ.get('SETTINGS'))

db = SQLAlchemy(app)
