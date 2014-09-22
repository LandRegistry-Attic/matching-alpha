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

@manager.option('--username', dest='username')
@manager.option('--rolename', dest='rolename')
def add_role_to_user(username, rolename):
    role = Role.query.filter_by(name=rolename).first()
    if not role:
        print "Couldn't find role", rolename
        return
    user = User.query.filter_by(name=username).first()
    if not user:
        print "Couldn't find user with username", username
        return
    else:
        if role not in user.roles:
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
        else:
            print "User %s already has role %s" % (user, role)

@manager.option('--name', dest='name')
@manager.option('--dob', dest='dob')
@manager.option('--gender', dest='gender')
@manager.option('--current_address', dest='current_address')
@manager.option('--previous_address', dest='previous_address')
def create_user(name, dob, gender, current_address,previous_address):
    if not User.query.filter_by(name=name).first():
        import datetime
        import uuid
        lrid = uuid.uuid4()
        print "User name %s does not exist so create it" % name
        date_of_birth = datetime.datetime.strptime(dob, '%Y-%m-%d')
        user = User(lrid=lrid,
                    name=name,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    current_address=current_address,
                    previous_address=previous_address)
        db.session.add(user)
        db.session.commit()
    else:
        print "User with name %s does exist so choose something else" % name

@manager.option('--lrid', dest='lrid')
def block_user(lrid):
    import uuid
    user_lrid = uuid.UUID(lrid)
    user = User.query.filter_by(lrid=user_lrid).first()
    if user:
        user.blocked = True

        db.session.add(user)
        db.session.commit()
        print "User %s has been blocked" % user.name
    else:
        print "User does not exist"

@manager.option('--lrid', dest='lrid')
def unblock_user(lrid):
    import uuid
    user_lrid = uuid.UUID(lrid)
    user = User.query.filter_by(lrid=user_lrid).first()
    if user:
        user.blocked = False

        db.session.add(user)
        db.session.commit()
        print "User %s has been unblocked" % user.name
    else:
        print "User does not exist"

if __name__ == '__main__':
    manager.run()
