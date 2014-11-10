import os
import sys
import struct

from get_int_price import GetIntPrice
from get_data_file_name import GetFileSourceName

usage = 'USAGE: EXEC SHORTCODE TRADING_DATE'

if (len(sys.argv) < 3):
	print usage
	exit(0)

shortcode = sys.argv[1]
trading_date = sys.argv[2]

data_file_name = GetFileSourceName(shortcode, trading_date)
data_file_name_original = data_file_name+'.original'

#os.system('/home/dvctrader/basetrade_install/bin/mkt_trade_logger SIM '+shortcode+' '+trading_date+' > '+data_file_name_original)

df_original = open(data_file_name_original, 'r')
df = open(data_file_name, 'wb')

p_timestamp = 0
p_type = '-'
p_bid_orders = 0
p_bid_size = 0
p_bid_price = 0
p_ask_price = 0
p_ask_size = 0
p_ask_orders = 0

for line in df_original:
	tokens = line.split()
	#for i in range(0, len(tokens)):
	#	print str(i)+' '+tokens[i]
	c_timestamp = tokens[0]
	[c_sec, c_usec] = tokens[0].split('.')
	c_sec = long(c_sec)
	c_usec = int(c_usec)
	c_type = tokens[1][2]
	c_bid_orders = int(tokens[-7])
	c_bid_size = int(tokens[-6])
	c_bid_price = GetIntPrice(shortcode, float(tokens[-5]))
	c_ask_price = GetIntPrice(shortcode, float(tokens[-4]))
	c_ask_size = int(tokens[-3])
	c_ask_orders = int(tokens[-2])
	if (c_type == 'T'):
		c_buysell = tokens[3]
		c_trade_size = int(tokens[4])
		c_trade_price = GetIntPrice(shortcode, float(tokens[6]))
	else:
		c_buysell = 'E'
		c_trade_size = 0
		c_trade_price = 0

	if (c_timestamp != p_timestamp or c_type != p_type or c_bid_size != p_bid_size or c_bid_price != p_bid_price 
					or c_ask_size != p_ask_size or c_ask_price != p_ask_price):
		df.write(struct.pack('QIccHHHHHH', c_sec, c_usec, c_type, c_buysell, c_bid_size, c_bid_price, c_ask_price, c_ask_size, 
							c_trade_size, c_trade_price))

	p_timestamp = c_timestamp
	p_type = c_type
	p_bid_orders = c_bid_orders
	p_bid_size = c_bid_size
	p_bid_price = c_bid_price
	p_ask_price = c_ask_price
	p_ask_size = c_ask_size
	p_ask_orders = c_ask_orders
	p_buysell = c_buysell
	p_trade_size = c_trade_size
	p_trade_price = c_trade_price

df.close()
df_original.close()
#os.system('rm -rf '+get_data_file_name(shortcode, trading_date)+'.original')