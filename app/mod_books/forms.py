#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description: Handle the Forms inside this module
# 
#############################################################
from flask import request
from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, SelectField, FileField, validators
from wtforms.validators import Required, EqualTo, Email, Length

from app.mod_users.constants import listKhuVuc, listNganhHoc, listTheLoaiSach, listTinhTrangSach

class searchBooks(Form):
	khuvuc = SelectField(u'Khu Vuc', choices=listKhuVuc)
  	chuyennganh = SelectField(u'Nganh Hoc', choices=listNganhHoc)
  	tensach = TextField('Ten Sach', [Required()])

class lienHeMua(Form):
	thoigian = TextField('Thoi gian')
	diadiem = TextField('Dia diem')
	lienhe = TextField('Lien he')
	#recaptcha = RecaptchaField()