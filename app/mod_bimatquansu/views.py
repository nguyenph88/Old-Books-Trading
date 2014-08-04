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

from app import db, lm
from app.mod_users.models import User

from app.mod_badges.constants import listBadges

###################################
## Initial setup for this module ##
###################################

# Register Blue print
mod = Blueprint('badges', __name__, url_prefix='/badges')

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

@mod.route('/update/')
def update():
  g.user.badges = '1,2,3'
  db.session.add(g.user)
  db.session.commit()
  flash(g.user.getBadgesList())
  badges = g.user.getBadgesList()
  return render_template("blank.html",badges=badges, listBadges=listBadges)
