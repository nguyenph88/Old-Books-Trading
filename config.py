#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description: All modules configuration
# Note: it will be different depends on the way we setup server
# 
#############################################################

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

# Indicates that it is a dev environment, you'll get the very helpful error page from flask when an error occurs.
DEBUG = False

# Contact email
ADMINS = frozenset(['peter.nguyen.csb@gmail.com'])
#  Will be used to sign cookies. Change it and all your users will have to login again
SECRET_KEY = 'conCOBEbe!@#anthit456conCHIMBUbu'

# Indicate we are going to use SQLITE
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Migration directory
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')

# I'm not sure what it is, someone says 2, others say 8
THREADS_PER_PAGE = 2

# Protect against form post
CSRF_ENABLED = True
CSRF_SESSION_KEY = "ConMa!ConMeo@ConMap$ConMu"

# RECAPTCHA setup for WTFORMS, Public/Private Keys obtain from Google Account
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
RECAPTCHA_OPTIONS = {'theme': 'white'}