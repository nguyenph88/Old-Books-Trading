#############################################################
# 
# Author: Peter Nguyen
# Last Update: 08/03/2014
# Description: Unchangable things linked to the "models.py"
# 
#############################################################

class Badges:
	name = ''
	imgName = ''
	
	def __init__(self, name, img):
		self.name = name
		self.imgName = img

listBadges = [Badges('NULL','NULL'),
			  Badges('KHTN TPHCM','dhkhtntphcm.png'),
			  Badges('Bach khoa', 'dhbktphcm.png'),
			  Badges('Donator', 'donator.png')]