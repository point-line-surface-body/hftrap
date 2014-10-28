import sys

def GetMinPriceIncrement(_shortcode_):
    if (_shortcode_ == 'ZN_0' or _shortcode_ == 'ZN_1'):
        return 0.015625
    elif (_shortcode_ == 'ZB_0'):
        return 0.031250
    else:
        return 0

def __main__(): 
    USAGE = "USAGE: EXEC SHORTCODE"
    if (len(sys.argv) < 2):
        print USAGE
        exit(0)       
    shortcode = sys.argv[1]
    print GetMinPriceIncrement(shortcode)
    
if __name__ == "__main__":
    __main__()