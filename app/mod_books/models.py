#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description:   - Model for this module
#                - Initialize with sqlite and basic column
# 
#############################################################
from app import db
from app.mod_users import constants as USER
import string, random
from hashlib import md5
 



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

    lienhemua = db.Column(db.SmallInteger, default=0)
    thoigiandang = db.Column(db.DateTime)
    # link to the user who posted this book
    # Foreign Key linked to a table then a specific field
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def get_id(self):
        return unicode(self.id)

    def get_short_title(self):
        if len(self.tensach) < 33:
            return self.tensach
        else:
            return (self.tensach[0:30] + "...")

    def __repr__(self):
        return '<Book %r>' % (self.tensach)