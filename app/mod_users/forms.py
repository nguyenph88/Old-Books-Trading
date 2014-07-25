#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description: Handle the Forms inside this module
# 
#############################################################

from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email, Length

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
  recaptcha = RecaptchaField()

class EditProfileForm(Form):
  fullname = TextField('FullName')
  email = TextField('Email address', [Email()])
  about_me = TextField('about_me', [Length(min = 0, max = 140)])
  recaptcha = RecaptchaField()  

class EditPasswordForm(Form):
  password = PasswordField('Password', [Required()])
  confirm = PasswordField('Repeat Password', [
      Required(),
      EqualTo('password', message='Passwords must match')
      ])
  recaptcha = RecaptchaField()  