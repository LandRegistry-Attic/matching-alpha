import os

from flask.ext.script import Manager
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand

from matching.models import *

from matching import app
from matching import db

app.config.from_object(os.environ['SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.option('--lrid', dest='lrid')
@manager.option('--name', dest='name')
@manager.option('--dob', dest='dob')
@manager.option('--gender', dest='gender')
@manager.option('--current_address', dest='current_address')
@manager.option('--previous_address', dest='previous_address')
def create_user(lrid, name, dob, gender, current_address,previous_address):

    import datetime
    import uuid
    lrid = uuid.UUID(lrid)

    if not User.query.get(lrid):
        date_of_birth = datetime.datetime.strptime(dob, '%Y-%M-%d')

        user = User(lrid=lrid,
                    name=name,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    current_address=current_address,
                    previous_address=previous_address)

        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    manager.run()
