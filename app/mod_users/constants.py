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

listKhuVuc = [('hcm', u'Miền Nam'), ('hn', u'Miền Trung'), ('tr', u'Miền Bắc')]
listNganhHoc = [('it', 'cong nghe thong tin'), ('ck', 'co khi'), ('dien', 'dien tu')]
