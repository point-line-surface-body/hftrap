import sys
from get_min_price_increment import get_min_price_increment

def get_int_price(shortcode, price):
	tick_size = get_min_price_increment(shortcode)
	if tick_size != 0:
		int_price = round((price/tick_size), 0)
	else:
		int_price = int(price)
	return int_price

def __main__():
	USAGE = 'USAGE: EXEC SHORTCODE PRICE'	
	if (len(sys.argv) < 3):
		print USAGE
		exit()
	shortcode = sys.argv[1]
	price = float(sys.argv[2])
	int_price = get_int_price(shortcode, price)
	print int_price

if __name__ == "__main__":
	__main__()
