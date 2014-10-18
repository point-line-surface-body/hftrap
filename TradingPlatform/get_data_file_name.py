import sys

def GetFileSourceName(shortcode, trading_date):
	return 'Data/'+shortcode+'.'+trading_date

def __main__():
	USAGE = 'USAGE: EXEC SHORTCODE TRADING_DATE'	
	if (len(sys.argv) < 3):
		print USAGE
		exit(0)
	shortcode = sys.argv[1]
	trading_date = sys.argv[2]	
	data_file_name = GetFileSourceName(shortcode, trading_date)
	print data_file_name
	
if __name__ == '__main__':
	__main__()
