import sqlalchemy
import re
import sys
import requests
import cookielib
import urllib
import socket
from struct import *
socket.setdefaulttimeout(10000)
reload(sys)
sys.setdefaultencoding("utf-8")

def visitPhones(page):
	pass

def amazon(url, i):
	print "Visiting ", str(i)
	print url
	p = re.compile(ur'class="pagnNext"\n*\s* href="(.*)">\n?\s*<span id="pagnNextString')
	headers = {
    'User-Agent': 'Mozilla/5.0'
    }	
	uf = requests.get(url, headers = headers)
	if uf.status_code == 200 :
		print uf.encoding
		print uf.text
		sys.exit()
		#good we are getting 200
		visitPhones(uf.text)
		match = re.search(p, uf.text)
		#check if more pages are pressent
		if match :
			amazon("http://www.amazon.in"+str(match.group(1)),i+1)
		else:
			print "done!"		
	else :
		print 'are u connected?'