#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description: Handle the Forms inside this module
# 
#############################################################

from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email

class LoginForm(Form):
  email = TextField('Emailaddress', [Required(), Email()])
  password = PasswordField('Password', [Required()])
  remember_me = BooleanField('remember_me', default = False)

class RegisterForm(Form):
  name = TextField('NickName', [Required()])
  email = TextField('Email address', [Required(), Email()])
  password = PasswordField('Password', [Required()])
  confirm = PasswordField('Repeat Password', [
      Required(),
      EqualTo('password', message='Passwords must match')
      ])
  accept_tos = BooleanField('I accept the TOS', [Required()])
  recaptcha = RecaptchaField()
