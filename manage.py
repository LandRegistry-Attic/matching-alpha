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

@manager.option('--name', dest='name')
def create_role(name):
    if not Role.query.filter_by(name=name).first():
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()

@manager.option('--userlrid', dest='userlrid')
@manager.option('--rolename', dest='rolename')
def add_role_to_user(userlrid, rolename):
    role = Role.query.filter_by(name=rolename).first()
    if not role:
        print "Couldn't find role", rolename
        return
    user = User.query.get(userlrid)
    if not user:
        print "Couldn't find user with lrid", lrid
        return
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()

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
        date_of_birth = datetime.datetime.strptime(dob, '%Y-%m-%d')

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
