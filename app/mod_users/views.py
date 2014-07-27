# -*- coding: utf-8 -*-
#############################################################
# 
# Author: Peter Nguyen, Hoc Duong
# Last Update: 07/26/2014
# Description:   - Define how each route is handled
#                - Handle all http/get/post requests
# 
#############################################################


from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user
from werkzeug import check_password_hash, generate_password_hash, secure_filename
from flask_wtf.file import FileField

from datetime import datetime
from flask.ext.babel import Babel
from app import db, lm, uf
from app.mod_users.forms import RegisterForm, LoginForm, EditProfileForm, EditPasswordForm, DangSach
from app.mod_users.models import User, Book

from datetime import datetime

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

@mod.before_request
def before_request():
  """
  pull user's profile from the database before every request are treated
  """
  g.user = None
  if 'user_id' in session:
    g.user = User.query.get(session['user_id'])
    # update last seen, does not necessary to update it in Login because sometimes user uses remember_me
    g.user.last_seen = datetime.utcnow()
    db.session.add(g.user)
    db.session.commit()

@mod.route('/ban-than/')
@login_required
def home():
  return render_template("users/profile.html", user=g.user, is_auth = g.user.is_authenticated(), username=g.user.nickname)

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
      session['username'] = user.nickname
      session['remember_me'] = form.remember_me.data

      # Get the remember_me option and save it to user, then empty it 
      remember_me = False
      if 'remember_me' in session:
          remember_me = session['remember_me']
          session.pop('remember_me', None)
      
      # log the user in using Flask-Login
      login_user(user, remember_me)

      flash('Welcome %s' % user.fullname)
      return redirect(url_for('users.home'))
    flash('Wrong email or password', 'error-message')
  return render_template("users/login.html", form=form)

@mod.route('/register/', methods=['GET', 'POST'])
def register():
  # If user is already login then redirect user to the profile page
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('users.home'))
  # Otherwise bring up the register form  
  form = RegisterForm(request.form)
  if form.validate_on_submit():
    # create an user instance not yet stored in the database
    user = User(nickname=form.nickname.data, fullname=form.fullname.data, email=form.email.data,\
      password=generate_password_hash(form.password.data))
    # Insert the record in our database and commit it
    db.session.add(user)
    db.session.commit()

    # Log the user in, as he now has an id and name
    session['user_id'] = user.id
    session['username'] = user.nickname

    # flash will display a message to the user
    flash('Thanks for registering')
    # redirect user to the 'home' method of the user module.
    return redirect(url_for('users.home'))
  return render_template("users/register.html", form=form)

@mod.route('/<nickname>')
@login_required
def thanhvien(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    return render_template('users/thanh-vien.html', user = user, is_auth = g.user.is_authenticated(), username = g.user.nickname)

@mod.route('/thay-doi-thong-tin/', methods = ['GET', 'POST'])
@login_required
def thaydoithongtin():
  editProfile = EditProfileForm(request.form)

  if editProfile.validate_on_submit():
    g.user.fullname = editProfile.fullname.data
    g.user.email = editProfile.email.data
    g.user.about_me = editProfile.about_me.data
    db.session.add(g.user)
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('users.home'))
  else:
    editProfile.fullname.data = g.user.fullname
    editProfile.email.data = g.user.email
    editProfile.about_me.data = g.user.about_me
  return render_template("users/thay-doi-thong-tin.html", editprofileform=editProfile,\
                          is_auth = g.user.is_authenticated(), username = g.user.nickname, user=g.user)
  #return render_template("users/thay-doi-thong-tin.html")

@mod.route('/thay-doi-mau-khau/', methods = ['GET', 'POST'])
@login_required
def thaydoimatkhau():
  editPassword = EditPasswordForm(request.form)

  if editPassword.validate_on_submit():
    g.user.password = editPassword.password.data
    db.session.add(g.user)
    db.session.commit()
    flash('Password changed successfully.')
    return redirect(url_for('users.home'))
  return render_template("users/thay-doi-mat-khau.html", editpasswordform=editPassword,\
                          is_auth = g.user.is_authenticated(), username = g.user.nickname)

@mod.route('/dang-sach/', methods=['GET', 'POST'])
@login_required
def dangsach():
  form = DangSach()
  if form.validate_on_submit():
    filename = secure_filename(form.imageFile.data.filename)
    validatefile = request.files['imageFile']
    # save the image only when user chooses a file
    if validatefile:
      form.imageFile.data.save(uf + filename)

    book = Book( truong=form.truong.data, khuvuc=request.form['khuvuc'], chuyennganh=request.form['chuyennganh'], giaovien=form.giaovien.data,\
        tensach=form.tensach.data, tacgia=form.tacgia.data, theloai=form.theloai.data, tinhtrang=form.tinhtrang.data, giaban=form.giaban.data, \
        noigapmat=form.noigapmat.data, thoigiangapmat=form.thoigiangapmat.data, lienhe=form.lienhe.data, \
        author=g.user, thoigiandang=datetime.utcnow())
    # Insert the record in our database and commit it
    db.session.add(book)
    db.session.commit()
    flash('book load already' + filename)
    return redirect(url_for('users.home'))
  return render_template("users/dang-sach.html", form=form, is_auth = g.user.is_authenticated(), username = g.user.nickname)

@mod.route('/dang-xuat/')
@login_required
def dangxuat():
  logout_user()
  session.clear()
  return render_template("users/dang-xuat.html")

