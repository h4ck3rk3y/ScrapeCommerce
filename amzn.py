import re
import sys
import requests
import cookielib
import socket
from struct import *
socket.setdefaulttimeout(10000)
reload(sys)
sys.setdefaultencoding("utf-8")

def visitPhones(phone_url, phone_id):
	result = []
	headers = {
	    'User-Agent': 'Mozilla/5.0'
	    }
	response = requests.get(phone_url, headers= headers)
	if response.status_code == 200:
		name = re.search('<span id="productTitle" class="a-size-large">(.*)</span>', response.text)
		picture = re.search('" data-old-hires="(.*)"  class=', response.text)
		desc = re.findall('<li><span class="a-list-item"> (.*)<\/span>', response.text)
		price = re.search(' <span class="a-size-mini"> <span class="currencyINR">&nbsp;&nbsp;</span>(.*)</span>', response.text)
		rating = re.search('class="reviewCountTextLinkedHistogram noUnderline" title="(\d*\.?\d*) out of 5 stars">', response.text)
		warranty = re.search('Warranty Details:<\/strong> (.*)\W*<\/span>', response.text)
		asin = re.search('asin=([A-Z0-9]*)&quot;',response.text)
		if asin.group(1) in phone_id :
			return False
		else :
			phone_id.append(asin.group(1))		
		if name and price and picture:
			result.append(name.group(1))
			result.append(picture.group(1))
			if desc:
				result.append(desc)
			else:
				result.append('Description not available.')
			result.append(str(price.group(1)).strip())
			if rating:
				result.append(rating.group(1))
			else :
				result.append('Rating not available!')
			if warranty:
				result.append(warranty.group(1))
			else :
				result.append('Warranty not available.')
			return result
		else :
			return False
	else:
		return False

def action(brand, keyword):
	phone_list = []
	phone_id = []
	for x in xrange(1,1000):
		url = 'http://www.amazon.in/s/ref=sr_pg_'+str(x)+'?fst=as%3Aoff&rh=n%3A976419031%2Cn%3A1389401031%2Cn%3A1389432031%2Cn%3A1805560031%2Ck%3A'+keyword+'%2Cp_89%3A'+brand+'&page=2&keywords='+keyword+'&ie=UTF8&qid=1430076551'
		headers = {
	    'User-Agent': 'Mozilla/5.0'
	    }	
		response = requests.get(url, headers = headers)
		if response.status_code == 200 :
			p = re.compile('a-text-normal" title=".*" href="(.*)"><h2')
			match = re.findall(p, response.text)
			if match :
				for phone in match:
					data = visitPhones(phone, phone_id)
					if data:
						print data
						phone_list.append(phone)
		else :
			print 'Done!/Bad connectivity!'

def amazon():
	brand = raw_input('Enter brand name\n')
	keyword =raw_input('Enter Keyword\n')
	action(brand, keyword)
