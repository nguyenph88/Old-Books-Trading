#############################################################
# 
# Author: Peter Nguyen, Hoc Duong
# Last Update: 07/22/2014
# Description:   - Model for this module
#                - Initialize with sqlite and basic column
# 
#############################################################

from app import db
from app.mod_users import constants as USER
import string, random
from hashlib import md5

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), unique=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)
    activation_code = db.Column(db.String(12), unique=True)
    # backref indicates that table Book can call the related user who posted by book.author
    books = db.relationship('Book', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime)

    badges = db.Column(db.String(100))

    sosachdang = db.Column(db.SmallInteger, default=0)
    sosachdaban = db.Column(db.SmallInteger, default=0)
    sosachdamua = db.Column(db.SmallInteger, default=0)
    
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def __init__(self, nickname=None, fullname=None, email=None, password=None, badges=None):
      self.nickname = nickname
      self.fullname = fullname
      self.email = email
      self.password = password
      self.badges = badges
      self.activation_code = self.activationkey_generator()

    def activationkey_generator(self):
      return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    def getBadgesList(self):
      if ',' not in self.badges:
        return [int(self.badges),0]
      else:
        return map(int,self.badges.split(','))

    def setNewBadge(self,num):
        self.badges = self.badges + ',' + str(num)

    def getStatus(self):
      return USER.STATUS[self.status]

    def getRole(self):
      return USER.ROLE[self.role]

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
        
    def __repr__(self):
        return '<User %r>' % (self.nickname)


