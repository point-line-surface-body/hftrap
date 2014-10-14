import sys

def get_min_price_increment(shortcode):
    if (shortcode == 'ZN_0' or shortcode == 'ZN_1'):
        return 0.015625 ;
    else:
        return 0

def __main__(): 
    USAGE = "USAGE: EXEC SHORTCODE"
    if (len(sys.argv) < 2):
        print USAGE
        exit(0)       
    shortcode = sys.argv[1]
    print get_min_price_increment(shortcode)
    
if __name__ == "__main__":
    __main__()
