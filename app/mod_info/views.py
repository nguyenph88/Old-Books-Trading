# -*- coding: utf-8 -*-
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
from flask.ext.login import login_required, login_user, logout_user

from app import db, lm
from app.mod_users.models import User

###################################
## Initial setup for this module ##
###################################

# Register Blue print
mod = Blueprint('info', __name__, url_prefix='/info')

# Set the page that @login_required will redirect to
lm.login_view = 'users.dangnhap'

# Display this message when user not login and try to connect to #login_required
lm.login_message = u"Xin vui lòng đăng nhập để tiếp tục."

###################################
########## View Handling ##########
###################################

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@mod.before_request
def before_request():
  """
  pull user's profile from the database before every request are treated
  """
  g.user = None
  if 'user_id' in session:
    g.user = User.query.get(session['user_id'])

def check_authenticate():
    usr = ""
    is_authenticated = False
    if 'user_id' in session:
        usr = session['username']
        is_authenticated = True
    return is_authenticated, usr

@mod.route('/gioi-thieu/')
def gioithieu():
  is_authenticated, usr = check_authenticate()
  return render_template("info/gioi-thieu.html", user=g.user, is_auth = is_authenticated, username=usr)

@mod.route('/huong-dan-su-dung/')
def huongdansudung():
  return render_template("info/huong-dan-su-dung.html")

@mod.route('/bao-mat/')
def baomat():
  return render_template("info/bao-mat.html")

@mod.route('/lien-he/')
def lienhe():
  return render_template("info/lien-he.html")

@mod.route('/quyen-loi-trach-nhiem/')
def quyenloitrachnhiem():
  return render_template("info/quyen-loi-trach-nhiem.html")