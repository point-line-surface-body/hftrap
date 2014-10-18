class ContractSpecification(object):
    def __init__(self, *argv):
        self.min_price_increment_ = 1.0
        self.numbers_to_dollars_ = 1.0
        self.exch_source_ = "INVALID"
        self.min_order_size_ = 1
        if len(argv) == 4 :
            self.min_price_increment_ = (float)(argv[0])
            self.numbers_to_dollars_ = (float)(argv[1])
            self.exch_source_ = argv[2]
            self.min_order_size_ = (int)(argv[3])
            
class SecurityDefinitions(object):
    
    @staticmethod
    def GetContractMinPriceIncrement(_shortcode_, _date_):
        if (_shortcode_ == 'ZN_0' or _shortcode_ == 'ZN_1'):
            return 0.015625
        else:
            return 0
    
    @staticmethod
    def GetContractMinOrderSize(_shortcode_, _date_):
        return 1

    @staticmethod
    def GetTradeBeforeQuote(_shortcode_, _date_):
        return  # not necessary to  implement ??
    
    @staticmethod
    def GetContractExchSource(_shortcode_, _date_):
        return

    @staticmethod
    def GetConfToMarketUpdateMsecs(_shortcode_, _date_):
        return