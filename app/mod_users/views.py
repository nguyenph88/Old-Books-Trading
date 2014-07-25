# -*- coding: utf-8 -*-
#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/22/2014
# Description:   - Define how each route is handled
#                - Handle all http/get/post requests
# 
#############################################################


from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user
from werkzeug import check_password_hash, generate_password_hash

from app import db, lm
from app.mod_users.forms import RegisterForm, LoginForm
from app.mod_users.models import User
from app.mod_users.decorators import requires_login

###################################
## Initial setup for this module ##
###################################

# Register Blue print
mod = Blueprint('users', __name__, url_prefix='/users')

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

@mod.route('/me/')
@login_required
def home():
  return render_template("users/profile.html", user=g.user, is_auth = g.user.is_authenticated(), username=g.user.name)

@mod.before_request
def before_request():
  """
  pull user's profile from the database before every request are treated
  """
  g.user = None
  if 'user_id' in session:
    g.user = User.query.get(session['user_id'])

@mod.route('/dang-nhap/', methods=['GET', 'POST'])
def dangnhap():
  # If user is already login then redirect user to the profile page
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('users.home'))

  form = LoginForm(request.form)
  # make sure data are valid, but doesn't validate password is right
  if form.validate_on_submit():
    # Check if the email is in the database, do not allow register
    user = User.query.filter_by(email=form.email.data).first()
    # we use werzeug to validate user's password
    if user and check_password_hash(user.password, form.password.data):
      # the session can't be modified as it's signed, 
      # it's a safe place to store the user id
      session['user_id'] = user.id
      session['username'] = user.name
      session['remember_me'] = form.remember_me.data

      # Get the remember_me option and save it to user, then empty it 
      remember_me = False
      if 'remember_me' in session:
          remember_me = session['remember_me']
          session.pop('remember_me', None)
      
      # log the user in using Flask-Login
      login_user(user, remember_me)

      flash('Welcome %s' % user.name)
      return redirect(url_for('users.home'))
    flash('Wrong email or password', 'error-message')
  return render_template("users/login.html", form=form)

@mod.route('/register/', methods=['GET', 'POST'])
def register():
  """
  Registration Form
  """
  # If user is already login then redirect user to the profile page
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('users.home'))
  # Otherwise bring up the register form  
  form = RegisterForm(request.form)
  if form.validate_on_submit():
    # create an user instance not yet stored in the database
    user = User(name=form.name.data, email=form.email.data, \
      password=generate_password_hash(form.password.data))
    # Insert the record in our database and commit it
    db.session.add(user)
    db.session.commit()

    # Log the user in, as he now has an id and name
    session['user_id'] = user.id
    session['username'] = user.name

    # flash will display a message to the user
    flash('Thanks for registering')
    # redirect user to the 'home' method of the user module.
    return redirect(url_for('users.home'))
  return render_template("users/register.html", form=form)

@mod.route('/dang-sach/')
def dangsach():
  form = RegisterForm(request.form)
  return render_template("users/dang-sach.html", form=form)

@mod.route('/dang-xuat/')
def dangxuat():
  logout_user()
  session.clear()
  return render_template("users/dang-xuat.html")
