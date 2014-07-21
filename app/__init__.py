#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description:   - Main setup for the app
#                - Initialize database type
#                - Register blueprints
#                - 404 error page
# 
#############################################################
import os
import sys

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

# Initialize the database, which will be using through all module using "from app import db"
db = SQLAlchemy(app)

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
@app.route('/')
def index():
    """Just a generic index page to show."""
    return render_template('index.html')

@app.route('/index.html')
def indexhtml():
    """Just a generic index page to show."""
    return render_template('index.html')

@app.route('/about-us.html')
def about_us():
    """Just a generic index page to show."""
    return render_template('about-us.html')


@app.errorhandler(404)
def not_found(error):
    """Handle 404 error page"""
    return render_template('404.html'), 404


##############################
### Define Blueprints here ###
##############################
from app.mod_users.views import mod as usersModule
app.register_blueprint(usersModule)

from app.mod_info.views import mod as infoModule
app.register_blueprint(infoModule)

from app.mod_newlistings.views import mod as newlistingsModule
app.register_blueprint(newlistingsModule)

# Commend this out if we are not manually create database in "shell.py"
#db.create_all()