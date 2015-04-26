import sqlalchemy
import re
import sys
import requests
import cookielib
import urllib
import time
import socket
from struct import *
socket.setdefaulttimeout(10000)
reload(sys)
sys.setdefaultencoding("utf-8")

def visitPhone(url, id_list):
	url = "http://flipkart.com" + url
	response = requests.get(url)
	output = []
	if response.status_code == 200:
		ids   = re.search("'identifier' : \"(.*)\"", response.text)
		if ids in id_list :
			return False
		else:
			id_list.append(ids)	
		name  = re.search("fn' : \"(.*)\",", response.text)
		photo = re.search("'photo' : \"(.*)\"", response.text)
		price = re.search('<meta itemprop="price" content="([0-9,]*)">',response.text)
		rating = re.search('<div class="fk-stars" title="(\d*\.?\d* stars)">',response.text)
		description = re.findall('<li class="key-specification tmargin2 bmargin2">(.*)<\/li>',response.text)
		warranty = re.search('span class="warranty-text">\W*(.*)\W*<\/span>',response.text)
		if name and photo and price :
			output.append(name.group(1))
			output.append(photo.group(1))
			output.append(price.group(1))
		else :
			return False
		if rating:
			output.append(rating.group(1))
		else :
			output.append('Not Rated')
		if description :
			output.append((description))
		else :
			output.append('No Description')	
		if warranty:
			output.append(warranty.group(1))
		else :
			output.append('No warranty information')
		return output			


def action(brand, keyword):
	phone_list = []
	id_list = []
	for x in xrange(0, 1000, 20) :
		time.sleep(10)
		url = 'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=facets.brand%255B%255D%3D'+brand+'&sid=tyy%2C4io&filterNone=true&start='+str(x)+'&q='+keyword+'&ajax=true&_=1430059919471'
		p = re.compile(ur'<a class="fk-display-block" data-tracking-id="prd_title" href="(.*)" title=".*">')
		response = requests.get(url)
		if response.status_code == 200 :
			if (response.text).find("No matching products available")!=-1:
				break
			else :
				match = re.findall(p, response.text)
				if match:
					for phone in match:
						data = visitPhone(phone, id_list)
						if data :
							phone_list.append(data)
							print data
				else :
					print 'nothing matched. check regex'		

		else :
			print 'Check Connectivity'				

def flipkart():
	brand = raw_input("Enter Brand Name:\n")
	keyword = raw_input("Enter Keyword:\n")
	action(brand, keyword)