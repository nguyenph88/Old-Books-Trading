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
    
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def __init__(self, nickname=None, fullname=None, email=None, password=None):
      self.nickname = nickname
      self.fullname = fullname
      self.email = email
      self.password = password
      self.activation_code = self.activationkey_generator()

    def activationkey_generator(self):
      return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

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
        return '<User %r>' % (self.name)


class Book(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key = True)
    truong = db.Column(db.String(100))
    khuvuc = db.Column(db.String(100))
    chuyennganh = db.Column(db.String(100))
    giaovien = db.Column(db.String(100))

    tensach = db.Column(db.String(100))
    tacgia = db.Column(db.String(100))
    theloai = db.Column(db.String(100))
    tinhtrang = db.Column(db.String(100))
    
    giaban = db.Column(db.SmallInteger, default=0)
    noigapmat = db.Column(db.String(300))
    thoigiangapmat = db.Column(db.String(200))
    lienhe = db.Column(db.String(200))
    image = db.Column(db.String(200))

    thoigiandang = db.Column(db.DateTime)
    # link to the user who posted this book
    # Foreign Key linked to a table then a specific field
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    '''
    def __init__(self, truong=None, khuvuc=None, chuyennganh=None, giaovien=None, \
                tensach=None, tacgia=None, theloai=None, tinhtrang=None, giaban=None, \
                noigapmat=None, thoigiangapmat=None, lienhe=None):
        this.truong = truong
        this.khuvuc = khuvuc
        this.chuyennganh = chuyennganh
        this.giaovien = giaovien
        this.tensach = tensach
        this.tacgia = tacgia
        this.theloai = theloai
        this.theloai = theloai
        this.tinhtrang = tinhtrang
        this.giaban = giaban
        this.noigapmat = noigapmat
        this.thoigiangapmat = thoigiangapmat
        this.lienhe = lienhe
    '''
    def __repr__(self):
        return '<Book %r>' % (self.body)