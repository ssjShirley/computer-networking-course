#coding=utf-8

import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getMD5(s):

	hl = hashlib.md5()
	hl.update(s.encode('utf-8'))
	return hl.hexdigest()
