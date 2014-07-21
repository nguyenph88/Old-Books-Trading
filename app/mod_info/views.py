#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/20/2014
# Description:   - Define how each route is handled
#                - Handle all http/get/post requests
# 
#############################################################


from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash

##### !!!!! Important !!!!!
mod = Blueprint('info', __name__, url_prefix='/info')

@mod.route('/gioi-thieu/')
def gioithieu():
  return render_template("info/gioi-thieu.html")

@mod.route('/huong-dan-su-dung/')
def huongdansudung():
  return render_template("info/huong-dan-su-dung.html")

@mod.route('/ho-tro/')
def hotro():
  return render_template("info/ho-tro.html")

@mod.route('/lien-he/')
def lienhe():
  return render_template("info/lien-he.html")

@mod.route('/quyen-loi-trach-nhiem/')
def quyenloitrachnhiem():
  return render_template("info/quyen-loi-trach-nhiem.html")