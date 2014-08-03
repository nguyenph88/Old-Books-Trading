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
from flask.ext.login import login_required

from app import db, lm, do_qsort_swap
from app.mod_users.models import User
from app.mod_books.models import Book
from datetime import datetime
from app.mod_books.forms import searchBooks, lienHeMua

###################################
## Initial setup for this module ##
###################################

# Register Blue print
mod = Blueprint('books', __name__, url_prefix='/books')

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

@mod.route('/')
def sachmoidang():
  books = Book.query.all()
  ltime = [b.thoigiandang for b in books]
  do_qsort_swap(ltime)
  lbooks = [Book.query.filter_by(thoigiandang = l).first() for l in ltime] 
  #return render_template("books/sachmoidang.html") 
  return render_template("books/sach-moi-dang.html", books=lbooks, is_auth = g.user.is_authenticated(), username = g.user.nickname)

@mod.route('/<bookid>')
def thongtinsach(bookid):
    book = Book.query.filter_by(id = bookid).first()
    if book == None:
        flash('Book ' + bookid + ' not found.')
        return redirect(url_for('books.sachmoidang'))
    return render_template('books/thong-tin-sach.html', book=book, is_auth = g.user.is_authenticated(), username = g.user.nickname)

@mod.route('/searchBooks/',  methods=['GET', 'POST'])
def searchbooks():
  form = searchBooks()
  if form.validate_on_submit():

    tensach = form.tensach.data
    khuvuc = form.khuvuc.data
    chuyennganh = form.chuyennganh.data

    lbooks = Book.query.filter(Book.tensach.like('%'+ tensach +'%'), Book.khuvuc.like('%'+ khuvuc +'%'), Book.chuyennganh.like('%'+ chuyennganh +'%') ).all()
    return render_template("books/searchBooks.html", form=form, books=lbooks, is_auth = g.user.is_authenticated(), username = g.user.nickname)
  return render_template('books/searchBooks.html',  form=form)

@mod.route('/lien-he-mua/<bookid>/')
def lienhemua(bookid):
    book = Book.query.filter_by(id = bookid).first()
    form = lienHeMua()

    if book == None:
        flash('Book ' + bookid + ' not found.')
        return redirect(url_for('books.sachmoidang'))
    elif book.author == g.user:
        flash(u'Bạn không thể mua sách của chính mình đăng.')
        return redirect(url_for('books.sachmoidang'))
    elif form.validate_on_submit():
        buyer_diadiem = form.diadiem.data
        buyer_thoigian = form.thoigian.data
        buyer_lienhe - form.lienhe.data
        # gui tat ca cac thong tin nay den email cua nguoi mua
        return redirect(url_for('books.sachmoidang'))
    return render_template('books/lien-he-mua.html', book=book, user = g.user, form=form, \
                            is_auth = g.user.is_authenticated(), username = g.user.nickname)
