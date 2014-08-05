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

# list of badges, remember to add to categorizeEmail if added more school
listBadges = [Badges('NULL','null.png'),
			  Badges(u'Sinh Viên của Đại Học Khoa Học Tự Nhiên TPHCM','dhkhtntphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Bách Khoa TPHCM', 'dhbktphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Kinh Tế TPHCM', 'dhkttphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Luật TPHCM', 'dhltphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Quốc Tế TPHCM', 'dhqttphcm.png'),
			  Badges(u'Sinh Viên của Đại Học RMIT TPHCM', 'dhrmittphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Sư Phạm TPHCM', 'dhsptphcm.png'),
			  Badges(u'Sinh Viên của Đại Học Y Dược TPHCM', 'dhydtphcm.png'),
			  Badges(u'Sinh Viên của Học Viện Bưu Chính Viễn Thông TPHCM', 'hvbcvttphcm.png'),
			  Badges(u'Có Đóng Góp Hỗ Trợ', 'donator.png')]

# categorize the email address to its appropriate school
def categorizeEmail(email):
    loai = email[email.index('@')+1 : len(email)]
    if loai == 'hcmus.edu.vn':
    	return '1'
    elif loai == 'hcmut.edu.vn':
    	return '2'
    elif loai == 'ueh.edu.vn':
    	return '3'    	
    elif loai == 'hcmulaw.edu.vn':
    	return '4'
    elif loai == 'hcmuiu.edu.vn':
    	return '5'
    elif loai == 'rmit.edu.vn':
    	return '6'
    elif loai == 'hcmup.edu.vn':
    	return '7'
    elif loai == 'yds.edu.vn':
    	return '8'
    elif loai == 'student.ptithcm.edu.vn':
    	return '9'
    else:
	    return '0'
