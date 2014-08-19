from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask.ext.mail import Mail, Message
from config import ADMINS
from threading import Thread
from app import mail
from flask.ext.mail import Mail, Message
 
#cerate new thread
def send_async_email(msg):
    mail.send(msg)

def send_email(subject, sender, recipients, html_body):

    mmsg = Message(subject, sender = sender, recipients = recipients)
    mmsg.html = html_body
    thr = Thread(target = send_async_email, args = [mmsg])
    thr.start()
# function that sends out email
def follower_notification(follow, file):
    nickname = follow.nickname.data
    nicknameFM = nickname.replace(" ", "%")
    send_email('chuyentay.vn',
        ADMINS[0],
        [follow.email.data],
        render_template(file, follower = nicknameFM))


def reset_password(follow, file, keys):
    send_email('chuyentay.vn',
        ADMINS[0],
        [follow.email.data],
        render_template(file, key = keys))

def buy_book(buyer, file, diaDiem, thoiGian, lienHe, book, sell, sendto):
    send_email('chuyentay.vn',
        ADMINS[0],
        [sendto.email],
        render_template(file, buyer = buyer, diadiem = diaDiem, thoigian = thoiGian, lienhe = lienHe, books = book, seller = sell))


