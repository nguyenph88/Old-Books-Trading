#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description:  Once the user is logged in we want to redirect the user to his profile (/users/me/). 
# 				To prevent unauthenticated users to access this page, we'll create a decorator to protect it 
# Note: This decorator is checking that g.user has a value assigned to it, otherwise it means that 
#		the user isn't authenticated, we then add a message to be displayed to the user on the 
#		next page and redirect him to the login view.
#
#  Important: g.user is defined in "views.py" -> "before_request"
# 
#############################################################

