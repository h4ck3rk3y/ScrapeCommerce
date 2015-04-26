from eby import ebay
from amzn import amazon
from fk import flipkart
from sdeal import snapdeal


def banner():
	print"""   ###    ##     ## ####  ######  ##     ##  ######  
  ## ##   ###   ###  ##  ##    ## ##     ## ##    ## 
 ##   ##  #### ####  ##  ##       ##     ## ##       
##     ## ## ### ##  ##  ##       ##     ##  ######  
######### ##     ##  ##  ##       ##     ##       ## 
##     ## ##     ##  ##  ##    ## ##     ## ##    ## 
##     ## ##     ## ####  ######   #######   ######  """
	print "Press 1 for Amazon"
	print "Press 2 for Snapdeal"
	print "Press 3 for Flipkart"
	print "Press 4 for Ebay"

def main():
	choice = int(raw_input(': '))
	if choice == 1 :
		amazon()
	elif choice == 2:
		snapdeal()
	elif choice == 3:
		flipkart()
	elif choice == 4:
		ebay()
	else:
		print  "Invalid Choice"
		main()



if __name__ == '__main__' :
	banner()
	main()
