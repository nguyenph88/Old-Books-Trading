#############################################################
# 
# Author: Peter Nguyen, Hoc Duong
# Last Update: 07/18/2014
# Description: Handle the Forms inside this module
# 
#############################################################
from flask import request
from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, SelectField, FileField, validators
from wtforms.validators import Required, EqualTo, Email, Length

from app.mod_users.constants import listKhuVuc, listNganhHoc, listTheLoaiSach, listTinhTrangSach

class LoginForm(Form):
  email = TextField('Emailaddress', [Required(), Email()])
  password = PasswordField('Password', [Required()])
  remember_me = BooleanField('remember_me', default = False)

class RegisterForm(Form):
  nickname = TextField('NickName', [Required()])
  fullname = TextField('FullName')
  email = TextField('Email address', [Required(), Email()])
  password = PasswordField('Password', [Required()])
  confirm = PasswordField('Repeat Password', [
      Required(),
      EqualTo('password', message='Passwords must match')
      ])
  accept_tos = BooleanField('I accept the TOS', [Required()])
  #recaptcha = RecaptchaField()

class EditProfileForm(Form):
  fullname = TextField('FullName')
  email = TextField('Email address', [Email()])
  about_me = TextField('about_me', [Length(min = 0, max = 140)])
  #recaptcha = RecaptchaField()  

class EditPasswordForm(Form):
  password = PasswordField('Password', [Required()])
  confirm = PasswordField('Repeat Password', [
      Required(),
      EqualTo('password', message='Passwords must match')
      ])
  #recaptcha = RecaptchaField()  

class DangSach(Form):
  truong = TextField('Truong Dang Hoc', [Required()])
  khuvuc = SelectField(u'Khu Vuc', choices=listKhuVuc)
  chuyennganh = SelectField(u'Nganh Hoc', choices=listNganhHoc)
  giaovien = TextField('Giao Vien', [Required()])

  tensach = TextField('Ten Sach', [Required()])
  tacgia = TextField('Ten Tac Gia', [Required()])
  theloai = SelectField(u'The Loai Sach', choices=listTheLoaiSach)
  tinhtrang = SelectField(u'Tinh trang sach', choices=listTinhTrangSach)
  giaban = TextField('Gia Ban', [Required()])
  thoigiangapmat = TextField('thoi gian va ngay hen', [Required()])
  noigapmat = TextField('Dia Diem Uu Tien', [Required()])
  lienhe = TextField('Lien He', [Required()])

  #myFile  = FileField(u'Image File', [validators.regexp(u'(?i)\.(jpg|png|gif)$')])
  imageFile  = FileField('Book image')

  accept_tos = BooleanField('I accept the TOS', [Required()])
  #recaptcha = RecaptchaField()



class forgot(Form):
  email = TextField('Email address', [Email()])
  

class getkey(Form):
  key =  TextField()







