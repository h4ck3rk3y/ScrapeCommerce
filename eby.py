import re
import sys
import requests
import cookielib
import urllib
import socket
from struct import *
from fuzzywuzzy import fuzz
socket.setdefaulttimeout(10000)
reload(sys)
sys.setdefaultencoding("utf-8")

def check(name, picture, desc, price, rating, warranty):
	name = name.group(1)
	if picture :
		picture = picture.group(1)
	else:
		picture = 'Picture Not Available'
	if desc:
		desc = desc.group(1)
	else :
		desc = 'Description not Available'
	if price:
		price = price.group(1)
	else:
		price = 'No Price Value'
	if rating:
		rating = rating.group(1)
	else:
		rating = "Review Not Available"
	if warranty:
		warranty = warranty.group(1)
	else :
		warranty = "Warranty Not Available"
	return [name, picture, desc, price, rating, warranty]	

def visitPhones(phone_url, phone_list):
	headers = {
	'User-Agent': 'Mozilla/5.0'
	}
	response = requests.get(phone_url)
	if response.status_code == 200 :
		price = re.search('<span class="notranslate" id="prcIsum" itemprop="price"  style="">(.*)</span>', response.text)
		picture = re.search("image.src= '(.*)';", response.text)
		name = re.search('<span id="vi-lkhdr-itmTitl" class="u-dspn">(.*)</span>', response.text)
		desc = re.search('features: <\/td>\W*<td width="50.0%">\W*<span>(.*)<\/span>', response.text)
		rating = re.search('<div id="si-fb" >(.*)%&nbsp;Positive feedback</div>', response.text)
		warranty = re.search('Warranty: <\/td>\W*<td width="50.0%">\W*<span>(.*)<\/span>', response.text)
		i = 0
		if name :
			for dictionary in phone_list:
				for key in dictionary.keys():
					if fuzz.ratio(key,name.group(1)) >= 60:
						phone_list[i][str(name.group(1))] = check(name, picture, desc, price, rating, warranty)
						return phone_list
				i = i + 1
			phone_list.append({})
			phone_list[len(phone_list)-1][str(name.group(1))] = check(name, picture, desc, price, rating, warranty)
			return phone_list
		else:
			return False

def action(brand, keyword):
	phone_list = []
	headers = {
	'User-Agent': 'Mozilla/5.0'
	}
	url = 'http://www.ebay.in/sch/Mobile-Phones-/15032/i.html?_from=R40&LH_AllListings=1&Brand='+brand+'&_sop=12&_nkw='+keyword+'&_pgn=1&_skc=200&rt=nc'
	response = requests.get(url, headers= headers)
	if response.status_code==200:
		rcnt = re.search('<span class="rcnt"  >(.*)</span>', response.text)
		if rcnt:
			rcnt = rcnt.group(1)
		else :
			return False
		rcnt = int(rcnt.replace(',',''))
		for x in xrange(1,int(rcnt/200.0)):
			url = 'http://www.ebay.in/sch/Mobile-Phones-/15032/i.html?_from=R40&LH_AllListings=1&Brand='+brand+'&_sop=12&_nkw='+keyword+'&_pgn='+str(x)+'&_skc=200&rt=nc'
			response = requests.get(url, headers=headers)
			if response.status_code == 200:
				p = re.compile('<h3 class="lvtitle"><a href="(.*)"\W*class')
				match = re.findall(p, response.text)
				if match:
					for x in match:
						visitPhones(x, phone_list)
				else:
					print 'Something is not right'
			else :
				'Something is not right!'
		print phone_list
	else:
		'Bad Connectivity!'
def ebay():
	brand = raw_input("Enter Brand Name:\n")
	keyword = raw_input("Enter Keyword:\n")
	action(brand, keyword)