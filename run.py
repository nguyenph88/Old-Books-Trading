#############################################################
# 
# Author: Peter Nguyen, duong binh hoc  12233333
# Last Update: 07/18/2014
# Description: Call this file in order to start the app
# 
#############################################################

from app import app
app.run(debug=True)

# Experiencing different local IP/port
#app.run(host='0.0.0.0', port=8080, debug=True)