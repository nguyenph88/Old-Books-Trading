# -*- coding: utf-8 -*-
#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/20/2014
# Description:   - Define how each route is handled
#                - Handle all http/get/post requests
# 
#############################################################


from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, app
from werkzeug import check_password_hash, generate_password_hash
from flask.ext.login import login_required
from app.mod_emails.views import buy_book
from app import db, lm
from app.mod_books.constants import do_qsort_swap
from app.mod_users.models import User
from app.mod_books.models import Book
from datetime import datetime
from app.mod_books.forms import searchBooks, lienHeMua
from app.mod_badges.constants import listBadges
import math   
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
  lbooks = [Book.query.filter_by(thoigiandang = l).first() for l in reversed(ltime)]
  leng = len(lbooks)/2
  return render_template("books/sach-moi-dang.html", books=lbooks, is_auth = g.user.is_authenticated(), username = g.user.nickname, length = leng, first =2)


num =0
@mod.route('/<bookid>')
def thongtinsach(bookid):
  if 'P' in bookid:
    global num
    s = ''.join(x for x in bookid if x.isdigit())
    if not s :
      if bookid == 'Pnext' :
        num +=2
      if bookid == 'Pback' :
        num -=2
    else : 
      num = int((int(s) +1)*2)
    books = Book.query.all()
    ltime = [b.thoigiandang for b in books]
    do_qsort_swap(ltime)

    lbooks = [Book.query.filter_by(thoigiandang = l).first() for l in reversed(ltime)]
    leng = len(lbooks)/2
    if num > len(lbooks) :
      num = len(lbooks)
    if num <= 0 :
      num = 2
    return render_template("books/sach-moi-dang.html", books=lbooks, is_auth = g.user.is_authenticated(), username = g.user.nickname, length = leng, first = num)
  else:
    
    book = Book.query.filter_by(id = bookid).first()
    if book == None:
        flash('Book ' + bookid + ' not found.')
        return redirect(url_for('books.sachmoidang'))
    return render_template('books/thong-tin-sach.html', book=book, listBadges=listBadges, badges=book.author.getBadgesList(), \
                            is_auth = g.user.is_authenticated(), username = g.user.nickname)


nums =0
lbooks = []
@mod.route('/searchBooks/',  methods=['GET', 'POST'])
@mod.route('/searchBooks/<bookid>')
def searchbooks(bookid="foo"):
  global nums
  global lbooks
  try:
    g.x
  except AttributeError:
    g.x=None
  form = searchBooks()
  if form.validate_on_submit():

    tensach = form.tensach.data
    khuvuc = form.khuvuc.data
    chuyennganh = form.chuyennganh.data
    if g.x is None:
      lbooks = Book.query.filter(Book.tensach.like('%'+ tensach +'%'), Book.khuvuc.like('%'+ khuvuc +'%'), Book.chuyennganh.like('%'+ chuyennganh +'%') ).all()
      g.x = lbooks
    leng = len(lbooks)/2
    return render_template("books/searchBooks.html", form=form, books=g.x, is_auth = g.user.is_authenticated(), username = g.user.nickname, length = leng, first =2)
  if 'P' in bookid:
    s = ''.join(x for x in bookid if x.isdigit())
    lbooks = g.x
    if not s :
      if bookid == 'Pnext' :
        nums +=2
      if bookid == 'Pback' :
        nums -=2
    else : 
      nums = int((int(s) +1)*2)
    leng = len(lbooks)/2
    if nums > len(lbooks) :
      nums = len(lbooks)
    if nums <= 0 :
      nums = 2
    flash('Book ' + bookid  )
    return render_template("books/searchBooks.html", form=form, books=g.x, is_auth = g.user.is_authenticated(), username = g.user.nickname, length = leng, first =nums)
  else :
    return render_template('books/searchBooks.html',  form=form, length = 0)

@mod.route('/lien-he-mua/<bookid>/',  methods=['GET', 'POST'])
def lienhemua(bookid):
    book = Book.query.filter_by(id = bookid).first()
    form = lienHeMua()

    if book == None:
        flash('Book ' + bookid + ' not found.')
        return redirect(url_for('books.sachmoidang'))
    elif book.author.nickname == g.user.nickname:
        flash(u'Bạn không thể mua sách của chính mình đăng.')
        return redirect(url_for('books.sachmoidang'))
    elif form.validate_on_submit():
        buyer_diadiem = form.diadiem.data
        buyer_thoigian = form.thoigian.data
        buyer_lienhe = form.lienhe.data
        # gui tat ca cac thong tin nay den email cua nguoi mua

        buy_book(g.user, 'emails/buybooks.html', buyer_diadiem, buyer_thoigian, buyer_lienhe, book, book.author, g.user )
        buy_book(g.user, 'emails/buybooks.html', buyer_diadiem, buyer_thoigian, buyer_lienhe, book, book.author,book.author)
        flash('da gui email cho nguoi ban va nguoi mua'  )
        return redirect(url_for('books.sachmoidang'))
    return render_template('books/lien-he-mua.html', book=book, user = g.user, form=form, \
                            is_auth = g.user.is_authenticated(), username = g.user.nickname)
