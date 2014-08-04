# -*- coding: utf-8 -*-
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
			  Badges(u'Sinh Viên của Đại Học Khoa Học Tự Nhiên TPHCM','dhkhtntphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Bách Khoa TPHCM', 'dhbktphcm.png'),

			  Badges(u'Sinh Viên của Đại Học Kinh Tế TPHCM', 'dhkttphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Luật TPHCM', 'dhltphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Quốc Tế TPHCM', 'dhqttphcm.png'),
			  Badges(u'Sinh Viên của Đại Học RMIT TPHCM', 'dhrmittphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Sư Phạm TPHCM', 'dhsptphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Y Dược TPHCM', 'dhydtphcm.png'),
			  Badges(u'Có Đóng Góp Hỗ Trợ', 'donator.png')]
