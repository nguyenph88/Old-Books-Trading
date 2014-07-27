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

from app import db, lm

###################################
## Initial setup for this module ##
###################################

# Register Blue print
mod = Blueprint('newlistings', __name__, url_prefix='/newlistings')

# Set the page that @login_required will redirect to
lm.login_view = 'users.dangnhap'

# Display this message when user not login and try to connect to #login_required
lm.login_message = u"Xin vui lòng đăng nhập để tiếp tục."

###################################
########## View Handling ##########
###################################
@mod.route('/')
def newlistings():
  return render_template("newlistings/newlistings.html")
