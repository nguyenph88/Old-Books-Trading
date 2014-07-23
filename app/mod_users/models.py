#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/22/2014
# Description:   - Model for this module
#                - Initialize with sqlite and basic column
# 
#############################################################

from app import db
from app.mod_users import constants as USER
import string, random

class User(db.Model):

    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)
    activation_code = db.Column(db.String(12), unique=True)
    # backref indicates that table Book can call the related user who posted by book.author
    books = db.relationship('Book', backref = 'author', lazy = 'dynamic')

    def __init__(self, name=None, email=None, password=None):
      self.name = name
      self.email = email
      self.password = password
      self.activation_code = self.activationkey_generator()

    def activationkey_generator(self):
      return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    def getStatus(self):
      return USER.STATUS[self.status]

    def getRole(self):
      return USER.ROLE[self.role]

    def __repr__(self):
        return '<User %r>' % (self.name)


class Book(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key = True)
    tensach = db.Column(db.String(100))
    tacgia = db.Column(db.String(100))
    truong = db.Column(db.String(100))
    chuyennganh = db.Column(db.String(100))
    giaovien = db.Column(db.String(100))
    giaban = db.Column(db.SmallInteger, default=0)
    tinhtrang = db.Column(db.String(100))
    thoigiandang = db.Column(db.DateTime)

    noigapmat = db.Column(db.String(300))
    thoigiangapmat = db.Column(db.String(200))
    lienhe = db.Column(db.String(200))
    # link to the user who posted this book
    # Foreign Key linked to a table then a specific field
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)