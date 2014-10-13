import sys
from Indicators.simple_trend import SimpleTrend

from TradingPlatform.data_file_constants import *
from get_data_file_name import get_data_file_name
#from get_time_from_timestamp import get_time_from_timestamp

usage = 'USAGE: EXEC SHORTCODE TRADING_DATE START_TIME END_TIME INDICATOR_LIST OUTPUT_FILE'

if (len(sys.argv) < 7):
	print usage
	exit(0)

shortcode = sys.argv[1]
trading_date = sys.argv[2]
start_time = sys.argv[3]
end_time = sys.argv[4]
indicator_list = sys.argv[5]
output_file = sys.argv[6]

data_file_name = get_data_file_name(shortcode, trading_date)

ilist = open(indicator_list, 'r')
indicators_strings = ilist.readlines()
ilist.close()

df = open(data_file_name, 'rb')
of = open(output_file, 'w')

indicators = []

for i in range(0, len(indicators_strings)):
	if (i < 3 or i == len(indicators_strings)-1):
		continue
	tokens = indicators_strings[i].split()
	if (tokens[2] == 'SimpleTrend'):
		indicators.append(SimpleTrend(tokens[3], tokens[4], tokens[5]))

while (1):
	timestamp = df.read(TIMESTAMP_SIZE)
	if (timestamp == ''):
		break
	update_type = df.read(TYPE_SIZE)
	bid_price = df.read(PRICE_SIZE)
	bid_size = df.read(SIZE_SIZE)
	bid_orders = df.read(ORDERS_SIZE)
	ask_price = df.read(PRICE_SIZE)
	ask_size = df.read(SIZE_SIZE)
	ask_orders = df.read(ORDERS_SIZE)

	output_string = str(timestamp)+' '+str(bid_price)+' '+str(bid_size)+' '+str(bid_orders)+' '+str(ask_price)+' '+str(ask_size)+' '+str(ask_orders)
	if (update_type == 0): # On Market Update
		for i in range(0, len(indicators)):
			indicator_value = indicators[i].OnMarketUpdate()
			output_string = output_string+' '+str(indicator_value)
		output_string = output_string+'\n'
	else: # On Trade Update
		for i in range(0, len(indicators)):
			indicator_value = indicators[i].OnTradeUpdate()
			output_string = output_string+' '+str(indicator_value)
		output_string = output_string+'\n'

	if (get_time_from_timestamp(timestamp) >= start_time): #@ashwin use the function from MathUtil , timestamp size is 4 only, so might not need any function here
		of.write(output_string)

	if (get_time_from_timestamp(timestamp) > end_time):
		break

of.close()
df.close()
