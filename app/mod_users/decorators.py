#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description:  Once the user is logged in we want to redirect the user to his profile (/users/me/). 
# 				To prevent unauthenticated users to access this page, we'll create a decorator to protect it 
# Note: This decorator is checking that g.user has a value assigned to it, otherwise it means that 
#		the user isn't authenticated, we then add a message to be displayed to the user on the 
#		next page and redirect him to the login view.
#
#  Important: g.user is defined in "views.py" -> "before_request"
# 
#############################################################

from functools import wraps

from flask import g, flash, redirect, url_for, request

def requires_login(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if g.user is None:
      flash(u'You need to be signed in for this page.')
      return redirect(url_for('users.login', next=request.path))
    return f(*args, **kwargs)
  return decorated_function