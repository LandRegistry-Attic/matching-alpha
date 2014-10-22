from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import BOOLEAN
from sqlalchemy.types import Enum


from matching import db

roles_users = db.Table('roles_users',
        db.Column('user_lrid',UUID(as_uuid=True), db.ForeignKey('users.lrid')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str({
            'name': self.name
        })

class User(db.Model):

    __tablename__ = 'users'

    lrid = db.Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    name = db.Column(TEXT, nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)
    gender = db.Column(Enum('F', 'M', name='gender_types'), nullable=False)
    current_address = db.Column(TEXT, nullable=False)
    previous_address = db.Column(TEXT, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return str({
            'lrid': self.lrid,
            'name': self.name,
            'date of birth': self.date_of_birth,
            'gender': self.gender,
            'current address': self.current_address,
            'previous address': self.previous_address,
            'roles': self.roles
        })
