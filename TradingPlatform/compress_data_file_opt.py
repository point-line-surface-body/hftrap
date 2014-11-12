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

df_original_file = open(data_file_name_original, 'r')
df_original = df_original_file.readlines()
df_original_file.close()
df = open(data_file_name, 'wb')

p_timestamp = 0
p_sec = 0
p_usec = 0
p_type = 'M'
p_buysell = 'B'
p_bid_orders = 0
p_bid_size = 0
p_bid_price = 0
p_ask_price = 0
p_ask_size = 0
p_ask_orders = 0
p_trade_price = 0
p_trade_size = 0

lines = 0
bid_size_state = 0
ask_size_state = 0



#--------------------------------------

# 
# minbp = 1000000000
# minap = 1000000000
# maxbp = 0
# maxap = 0
# for line in df_original:
#     tokens = line.split()
#     bp = GetIntPrice(shortcode, float(tokens[-5]))
#     ap = GetIntPrice(shortcode, float(tokens[-4]))
#     minbp = min(minbp, bp)
#     maxbp = max(maxbp, bp)
#     minap = min(minap, ap)
#     maxap = max(maxap, ap)
# 
# if (maxbp - minbp > 255):
#     print 'Cannot compress: bp '+str(maxbp)+' '+str(minbp)+' '+shortcode+' '+trading_date
#     exit(0)
# if (maxap - minap > 255):
#     print 'Cannot compress: ap '+str(maxap)+' '+str(minap)+' '+shortcode+' '+trading_date
#     exit(0)

# r_bid_price = minbp
# r_ask_price = minap
#--------------------------------------
r_tokens = df_original[0].split()
r_sec = long(r_tokens[0].split('.')[0])
df.write(struct.pack('Q', r_sec))

for line in df_original:
    tokens = line.split()
    #for i in range(0, len(tokens)):
    #    print str(i)+' '+tokens[i]
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
        
    to_write = 0
    if (c_type != p_type or c_bid_price != p_bid_price 
                    or c_ask_price != p_ask_price):
        to_write = 1
        if (c_bid_price != p_bid_price):
            bid_size_state = 0
        if (c_ask_price != p_ask_price):
            ask_size_state = 0
        
    else:
        if (c_bid_size != p_bid_size):
            if (bid_size_state == 0):
                to_write = 1
            if (bid_size_state == 1):
                if (c_bid_size < p_bid_size):
                    to_write = -1
            if (bid_size_state == 2):
                if (c_bid_size > p_bid_size):
                    to_write = -1
                
            if (c_bid_size > p_bid_size):
                bid_size_state = 1
            else:
                bid_size_state = 2
                
        elif (c_ask_size != p_ask_size):
            if (ask_size_state == 0):
                to_write = 1
            if (ask_size_state == 1):
                if (c_ask_size < p_ask_size):
                    to_write = -1
            if (ask_size_state == 2):
                if (c_ask_size > p_ask_size):
                    to_write = -1
                
            if (c_ask_size > p_ask_size):
                ask_size_state = 1
            else:
                ask_size_state = 2
        else:
            pass
        
    if (to_write == 1):
        lines += 1
        #print line
        df.write(struct.pack('IIccHHHHHH', c_sec-r_sec, c_usec, c_type, c_buysell, c_bid_size, c_bid_price, c_ask_price, c_ask_size, 
                            c_trade_size, c_trade_price))
    if (to_write == -1):
        lines += 1
        print p_sec-r_sec, p_usec, p_type, p_buysell, p_bid_size, p_bid_price, p_ask_price, p_ask_size, p_trade_size, p_trade_price
        df.write(struct.pack('IIccHHHHHH', p_sec-r_sec, p_usec, p_type, p_buysell, p_bid_size, p_bid_price, p_ask_price, p_ask_size, 
                            p_trade_size, p_trade_price))
    p_timestamp = c_timestamp
    p_sec = c_sec
    p_usec = c_usec
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

print lines
df.close()
#os.system('rm -rf '+get_data_file_name(shortcode, trading_date)+'.original')