import sys
from get_min_price_increment import GetMinPriceIncrement

def GetIntPrice(_shortcode_, _price_):
	tick_size = GetMinPriceIncrement(_shortcode_)
	if tick_size != 0:
		int_price = int(round((_price_/tick_size), 0))
	else:
		int_price = int(_price_)
	return int_price

def __main__():
	USAGE = 'USAGE: EXEC SHORTCODE PRICE'	
	if (len(sys.argv) < 3):
		print USAGE
		exit()
	shortcode = sys.argv[1]
	price = float(sys.argv[2])
	int_price = GetIntPrice(shortcode, price)
	print int_price

if __name__ == "__main__":
	__main__()
