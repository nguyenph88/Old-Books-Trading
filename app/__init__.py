#############################################################
# 
# Author: Peter Nguyen, Hoc Duong
# Last Update: 07/18/2014
# Description:   - Main setup for the app
#                - Initialize database type
#                - Register blueprints
#                - 404 error page
#                - 500 error page
# 
#############################################################
import os
import sys

from flask import Flask, render_template, g, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required
from flask.ext.mail import Mail, Message
from config import ADMINS
from threading import Thread

app = Flask(__name__)
app.config.from_object('config')

# Initialize the database, which will be using through all module using "from app import db"
db = SQLAlchemy(app)

#Initialize the email
mail = Mail(app)

# Initialize login manager to manager user session login
lm = LoginManager()
lm.init_app(app)

# Upload Folder
uf = app.config['UPLOAD_FOLDER']

#function that sends out email
def send_async_email(msg):
    mail.send(msg)


def send_email(subject, sender, recipients, html_body):

    mmsg = Message(subject, sender = sender, recipients = recipients)
    mmsg.html = html_body
    thr = Thread(target = send_async_email, args = [mmsg])
    thr.start()

def follower_notification(follower):
    send_email('chuyentay.vn',
        ADMINS[0],
        ['hocdb@student.ptithcm.edu.vn'],
        render_template("follower_email.html", follower = follower))
############################
### Configure Secret Key ###
############################
def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)

    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}/SECRET_KEY'.format(filename=full_path))
        sys.exit(1)

if not app.config['DEBUG']:
    install_secret_key(app)

############################
### Handle simple routes ###
############################
def check_authenticate():
    usr = ""
    is_authenticated = False
    if 'user_id' in session:
        usr = session['username']
        is_authenticated = True
    return is_authenticated, usr

@app.route('/index.html')
@app.route('/')
def index():
    """Just a generic index page to show."""
    is_authenticated, usr = check_authenticate()
    return render_template("index.html", is_auth=is_authenticated, username=usr)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 error page"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

##############################
### Define Blueprints here ###
##############################
from app.mod_users.views import mod as usersModule
app.register_blueprint(usersModule)

from app.mod_info.views import mod as infoModule
app.register_blueprint(infoModule)

from app.mod_books.views import mod as booksModule
app.register_blueprint(booksModule)

# Commend this out if we are not manually create database in "shell.py"
#db.create_all()