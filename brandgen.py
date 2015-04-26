import re
f = open("snapdeal.txt",'r')

p = re.compile('input id="Brand-([a-zA-Z0-9]*)"\n*')
print '[',
for line in f:
	match = re.findall(p,line)
	if match :
		print "'",match[0],"',",
print ']'