import sqlalchemy
import re
import sys
import requests
import cookielib
import socket
import json
from struct import *
socket.setdefaulttimeout(10000)
reload(sys)
sys.setdefaultencoding("utf-8")
def warranty(table):
	for data in table:
		if (data.lower()).find('warranty'):
			return True
	return False
def getWarranty(url):
	url = 'http://www.snapdeal.com' + url
	headers = {
    'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url,headers=headers)
def action(brand, keyword):
	result = []
	ids = []
	for starting_at in xrange(0,10000,49):
		url = 'http://www.snapdeal.com/acors/json/product/get/search/175/'+str(starting_at)+'/50?q=Brand%3A'+brand+'%7C&sort=rlvncy&keyword='+keyword+'&clickSrc=suggested&viewType=List&lang=en&snr=false'
		uf = requests.get(url)
		if uf.status_code == 200 :
			table = json.loads(uf.text)
			if table['status'] == 'Fail' :
				break
			table = table['productOfferGroupDtos']
			for x in table:
				output = [
				x['highlights'],
				x['id'],
				x['name'],
				x['avgRating'],
				x['noOfReviews'],
				x['image'],
				x['pageUrl'],
				]
				if x['id'] not in ids :
			 		ids.append(x['id'])
			 		result.append(output)
					if warranty(x['highlights']) :
						output.append(warranty)
					else:
						output.append(getWarranty(x['pageUrl']))	
					if 'displayPrice' in x.keys():
						output.append(x['displayPrice'])
					elif 'price' in x.keys():
						output.append(x['price'])
					else :
						output.append("No Price Data")
		else :
			print 'Not being able to reach snapdeal'
			break
	print str(len(result)) + " phones found!"

def snapdeal():
	brand_table = [ ' Micromax ', ' Samsung ', ' Apple ', ' HTC ', ' Karbonn ', ' Lenovo ', ' Xolo ', ' Panasonic ', ' Sony ', ' Adcom ', ' Agtel ', ' Alcatel ', ' Blackberry ', ' Celkon ', ' Cheers ', ' Chilli ', ' Forme ', ' Gfive ', ' Gionee ', ' Haier ', ' Huawei ', ' IDEA ', ' INEW ', ' Ikon ', ' Intex ', ' Kenxinda ', ' LG ', ' Lava ', ' Lima ', ' MTech ', ' Nikcron ', ' Nokia ', ' Obi ', ' Oppo ', ' Other ', ' Philips ', ' RRISHTA ', ' Reliance ', ' Rio ', ' SSK ', ' Spice ', ' Subway ', ' Swipe ', ' Videocon ', ' Vox ', ' Wham ', ' Wiio ', ' Zen ', ' iBall ', ]
	for brand in brand_table:
		print brand.strip()
	brand = raw_input("Enter Brand Name From List Above:\n")
	keyword = raw_input("Enter KeyWord:\n")
	print 'Begining Search'
	action(brand,keyword)