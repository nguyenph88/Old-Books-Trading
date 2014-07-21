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
mod = Blueprint('newlistings', __name__, url_prefix='/newlistings')

@mod.route('/')
def newlistings():
  return render_template("newlistings/newlistings.html")
