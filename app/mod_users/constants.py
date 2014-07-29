# -*- coding: utf-8 -*-
#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description: Unchangable things linked to the "models.py"
# 
#############################################################

# User role
ADMIN = 0
STAFF = 1
USER = 2
ROLE = {
  ADMIN: 'admin',
  STAFF: 'staff',
  USER: 'user',
}

# user status
INACTIVE = 0
NEW = 1
ACTIVE = 2
STATUS = {
  INACTIVE: 'inactive',
  NEW: 'new',
  ACTIVE: 'active',
}

listKhuVuc = [(u'Miền Nam', u'Miền Nam'), (u'Miền Trung', u'Miền Trung'), (u'Miền Bắc', u'Miền Bắc'), (u'Khác', u'Khác')]
listNganhHoc = [(u'Công Nghệ Thông Tin', u'Công Nghệ Thông Tin'), (u'Cơ Khí', u'Cơ Khí'), (u'Điện Tử', u'Điện Tử'), (u'Khác', u'Khác')]
listTheLoaiSach = [(u'Sách Giáo Khoa', u'Sách Giáo Khoa'), (u'Sách Tham Khảo', u'Sách Tham Khảo'), (u'Sách Giải', u'Sách Giải'), (u'Tài Liệu', u'Tài Liệu'), (u'Truyện', u'Truyện'), (u'Khác', u'Khác')]
listTinhTrangSach = [(u'Mới',u'Mới'), (u'Hơi Mới',u'Hơi Mới'), (u'Xài Được',u'Xài Được'), (u'Hơi Cũ',u'Hơi Cũ'), (u'Cũ',u'Cũ'), (u'Khác', u'Khác')]
