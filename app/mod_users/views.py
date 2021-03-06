# -*- coding: utf-8 -*-
#############################################################
# 
# Author: Peter Nguyen, Hoc Duong
# Last Update: 07/26/2014
# Description:   - Define how each route is handled
#                - Handle all http/get/post requests
# 
#############################################################


from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, app
from flask.ext.login import login_required, login_user, logout_user
from werkzeug import check_password_hash, generate_password_hash, secure_filename
from flask_wtf.file import FileField
from app.mod_emails.views import follower_notification, reset_password
from datetime import datetime, timedelta
from flask.ext.babel import Babel
from app import db, lm, uf, id_generator
from app.mod_users.forms import RegisterForm, LoginForm, EditProfileForm, EditPasswordForm, DangSach, forgot, getkey
from app.mod_books.models import Book
from app.mod_badges.constants import listBadges, categorizeEmail
from datetime import datetime
from app.mod_users.models import User
from app.mod_users import constants as USER
import os

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

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
  #return render_template("users/profile.html", user=g.user, is_auth = g.user.is_authenticated(), username=g.user.nickname)
  
  return redirect(url_for('users.thanhvien', nickname=g.user.nickname))

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
      if user.status == 2 :
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
        login_user(user, remember = remember_me)

        flash(u'Đăng nhập thành công. Xin chào %s' % user.fullname)
        return redirect(url_for('users.home'))
      else :
        flash(u'Tài Khoan Của Bạn Chưa Xác Thực', 'error-message')
        return render_template("users/login.html", form=form)
    flash(u'Sai Email hoặc Mật khẩu', 'error-message')
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
      password=generate_password_hash(form.password.data), badges=categorizeEmail(form.email.data))
    # Insert the record in our database and commit it
    user.status =0
    try:
      db.session.add(user)
      db.session.commit()
    except:
      db.session.rollback()
      flash('Email hoac nickname bi trung')
      return render_template("users/register.html", form=form)

    # Log the user in, as he now has an id and name---> allow login when verify already, so not set the session
    #session['user_id'] = user.id
    #session['username'] = user.nickname
    #send email to verify
    
    follower_notification(form, 'follower_email.html')
    # flash will display a message to the user
    # flash('Thanks for registering')
    # redirect user to the 'home' method of the user module.
    flash('chuyentay.com has been send email co your email adress, please visit to verify your account')
    return redirect(url_for('users.home'))
  return render_template("users/register.html", form=form)

@mod.route('/<nickname>')
@login_required
def thanhvien(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash(u'Thành viên ' + nickname + u' không tồn tại.')
        return redirect(url_for('index'))
    return render_template('users/thanh-vien.html', user = user, is_auth = g.user.is_authenticated(), \
                            username = g.user.nickname, books=g.user.books, \
                            listBadges=listBadges, badges=g.user.getBadgesList())

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
    validatefile = request.files['imageFile']
    # save the image only when user chooses a file
    if validatefile and allowed_file(validatefile.filename):
      filename = id_generator() +  secure_filename(form.imageFile.data.filename)
      form.imageFile.data.save(uf + filename)
    else:
      flash('please choose image File')
      return render_template("users/dang-sach.html", form=form, is_auth = g.user.is_authenticated(), username = g.user.nickname)
    book = Book( truong=form.truong.data, khuvuc=request.form['khuvuc'], chuyennganh=request.form['chuyennganh'], giaovien=form.giaovien.data,\
        tensach=form.tensach.data, tacgia=form.tacgia.data, theloai=form.theloai.data, tinhtrang=form.tinhtrang.data, giaban=form.giaban.data, \
        noigapmat=form.noigapmat.data, thoigiangapmat=form.thoigiangapmat.data, lienhe=form.lienhe.data, \
        author=g.user, thoigiandang=datetime.utcnow(), image=(filename))
    # Insert the record in our database and commit it
    db.session.add(book)
    db.session.commit()

    # Update number of books in db of that user
    g.user.sosachdang = g.user.sosachdang + 1
    db.session.add(g.user)
    db.session.commit()
    
    flash(u'Đăng Sách Thành Công! ' )
    return redirect(url_for('users.home'))
  return render_template("users/dang-sach.html", form=form, is_auth = g.user.is_authenticated(), username = g.user.nickname)

@mod.route('/sach-da-dang/', methods=['GET', 'POST'])
@login_required
def sachdadang():
  return render_template("users/sach-da-dang.html", is_auth = g.user.is_authenticated(), username = g.user.nickname, books=g.user.books)

@mod.route('/<nickname>/sach-da-dang/', methods=['GET', 'POST'])
@login_required
def sachdadangpublic(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash(u'Thành viên ' + nickname + u' không tồn tại.')
        return redirect(url_for('index'))
    return render_template("users/sach-da-dang-public.html", is_auth = g.user.is_authenticated(), username = g.user.nickname, books=user.books)

@mod.route('/sua-thong-tin-sach/<bookid>/', methods = ['GET', 'POST'])
@login_required
def suathongtinsach(bookid):
  form = DangSach()
  book = Book.query.get(bookid)

  # Check if the book is not owned by user, then redirect to users.home
  if book not in g.user.books:
    flash(u"Bạn không sở hữu sách này")
    return redirect(url_for('users.home'))
  # This is the book is owned by user
  elif form.validate_on_submit():
        book.truong = form.truong.data
        book.khuvuc = request.form['khuvuc']
        book.chuyennganh = request.form['chuyennganh']
        book.giaovien = form.giaovien.data

        book.tensach = form.tensach.data
        book.tacgia = form.tacgia.data
        book.theloai = request.form['theloai']
        book.tinhtrang = request.form['tinhtrang']
        book.giaban = form.giaban.data
        book.noigapmat = form.noigapmat.data
        book.thoigiangapmat = form.thoigiangapmat.data
        book.lienhe = form.lienhe.data
        book.thoigiandang = datetime.utcnow()

        '''
        # Handling file upload
        filename = secure_filename(form.imageFile.data.filename)
        validatefile = request.files['imageFile']
        # save the image only when user chooses a file, otherwise keep the same picture
        if validatefile:
          form.imageFile.data.save(uf + filename)
          book.image = filename
        '''
        # Overwrite the current book in database
        validatefile = request.files['imageFile']
        if validatefile and allowed_file(validatefile.filename):
          os.remove(uf + book.image)
          filename = id_generator() + secure_filename(form.imageFile.data.filename)
          form.imageFile.data.save(uf + filename)
          book.image = filename
        db.session.add(book)
        db.session.commit()
        
        flash(u'Cập Nhật Thông Tin Sách Thành Công!')
        return redirect(url_for('users.sachdadang'))
  else:
    form.truong.data = book.truong
    form.giaovien.data = book.giaovien
    form.tensach.data = book.tensach
    form.tacgia.data = book.tacgia
    form.giaban.data = book.giaban
    form.noigapmat.data = book.noigapmat
    form.thoigiangapmat.data = book.thoigiangapmat
    form.lienhe.data = book.lienhe

  return render_template("users/sua-thong-tin-sach.html", form=form, is_auth = g.user.is_authenticated(), username = g.user.nickname, \
                          last_image=book.image)

@mod.route('/xoa-sach/<bookid>/', methods = ['GET', 'POST'])
@login_required
def xoasach(bookid):
  book = Book.query.get(bookid)
  if book not in g.user.books:
    flash(u"Bạn không sở hữu sách này")
    return redirect(url_for('users.home'))
  else:
    # remove the book from list
    
    os.remove(uf + book.image)
    db.session.delete(book)
    # Update number of books in db of that user
    g.user.sosachdang = g.user.sosachdang - 1
    db.session.add(g.user)

    db.session.commit()

    flash(u"Bạn da xoa sach")
    return render_template("users/sach-da-dang.html", is_auth = g.user.is_authenticated(), username = g.user.nickname, books=g.user.books)

@mod.route('/dang-xuat/')
@login_required
def dangxuat():
  logout_user()
  return redirect(url_for('users.dangnhap'))

#test send email
@mod.route('/email/')
def send_email():
 #user = User.query.filter_by(nickname = nickname).first()
    # ...
    #follower_notification(g.user, 'follower_email.html')
    #flash('chuyentay.com has been send email co your email adress, please visit to verify your account')
    #return redirect(url_for('users.home'))
    flash('verify account ' + g.user.password)
    return redirect(url_for('users.home'))


#verify from user's email
@mod.route('/verify/<nickname>')
def verify(nickname):
  nicknameFM = nickname.replace("%", " ")
  user = User.query.filter_by(nickname = nicknameFM).first()
  user.status = 2
  db.session.add(user)
  db.session.commit()
  flash('account  ' + USER.STATUS[user.status])
  return redirect(url_for('users.home'))




@mod.route('/dang-nhap/forgot/', methods = ['GET', 'POST'])
def changepass():
    form = forgot()
    form1 = getkey()
    if form.validate_on_submit():
      user = User.query.filter_by(email = form.email.data).first()
      if user :
          keys = id_generator()
          session['key'] = keys
          session['email'] = user.email
          
          reset_password(form, 'resetpass.html', keys)
          k = "o"       
          flash('chuyentay.com has been send email co your email adress, please visit to change your password')
          #form1 = getkey()
          return render_template("users/getkey.html",  form=form1)
      else :
        flash('email nay khong co trong he thong')
        return render_template("users/forgot.html",  form=form )

    if form1.validate_on_submit():
        email = session['email']
        keys = session['key']
        user = User.query.filter_by(email = email).first()
        if form1.key.data ==  session['key'] :
          user.password = generate_password_hash(form1.key.data)
          db.session.add(user)
          db.session.commit()
          flash('ban da thay doi mat khau thanh cong'+ session['key'])
          return redirect(url_for('users.home')) 
        else :
          flash('key khong hop le'+ session['key'] + user.password)
          return redirect(url_for('users.home')) 

    else :
      return render_template("users/forgot.html",  form=form )

