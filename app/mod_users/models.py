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

    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)
    activation_code = db.Column(db.String(12), unique=True)

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