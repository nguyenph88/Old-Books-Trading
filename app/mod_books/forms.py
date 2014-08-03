#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description: Handle the Forms inside this module
# 
#############################################################
from flask import request
from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, validators, RadioField
from wtforms.validators import Required, EqualTo, Email, Length

class TimSach(Form):
  tensach = TextField('Truong Dang Hoc')
  #recaptcha = RecaptchaField()







