# -*- coding: utf-8 -*-
#############################################################
# 
# Author: Peter Nguyen
# Last Update: 08/03/2014
# Description:   - Define how each route is handled
#                - Handle all http/get/post requests
# 
#############################################################
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from app import db, lm
from app.mod_users.models import User

from app.mod_badges.constants import listBadges, categorizeEmail

###################################
## Initial setup for this module ##
###################################

# Register Blue print
mod = Blueprint('bimatquansu', __name__, url_prefix='/bimatquansu')

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

####################################
# Set new badge to a specific user #
####################################
@mod.route('/set-badge/')
def setbadge():
  nickname = 'hello'
  user = User.query.filter_by(nickname = nickname).first()
  user.setNewBadge(7)
  db.session.add(user)
  db.session.commit()
  flash(user.getBadgesList())
  badges = user.getBadgesList()
  return render_template("/bimatquansu/blank.html",badges=badges, listBadges=listBadges)

##########################################################
# Automatically add user to the database with given info #
##########################################################
@mod.route('/add-user/')
def adduser():
  nickname = 'cb5'
  fullname = 'Tran Van Huan'
  email = 'cc5@rmit.edu.vn'
  password = 'asd'
  badges = categorizeEmail(email)

  user = User(nickname=nickname, fullname=fullname, email=email,\
      password=generate_password_hash(password), badges=badges)
  db.session.add(user)
  db.session.commit()
  flash('created ' + nickname)
  return render_template("/bimatquansu/blank.html")