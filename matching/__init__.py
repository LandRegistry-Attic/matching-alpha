import os
import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from .health import Health

app = Flask(__name__)

app.config.from_object(os.environ.get('SETTINGS'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

app.logger.debug("\nConfiguration\n%s\n" % app.config)


def health(self):
    try:
        with self.engine.connect() as c:
            c.execute('select 1=1').fetchall()
            return True, 'DB'
    except:
        return False, 'DB'

SQLAlchemy.health = health

db = SQLAlchemy(app)
Health(app, checks=[db.health])
