#!/usr/bin/env python
#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description: will allow you to get a console and enter commands within your flask environment
#
# How to use:
#	user@Machine:~/Projects/dev$ . env/bin/activate
#	(env)user@Machine:~/Projects/dev$ python shell.py 
#	>>> from app import db
#	>>> db.create_all()
#	>>> exit()
#	(env)user@Machine:~/Projects/dev$ python run.py 
# 
#############################################################

import os
import readline
from pprint import pprint

from flask import *
from app import *

os.environ['PYTHONINSPECT'] = 'True'