
#Keeping only 1 Level in the book
class OrderBook:
    
    def __init__(self, bid_px, bid_sz, ask_px, ask_sz):
        self._bid_price_ = bid_px
        self._bid_size_ = bid_sz
        self._ask_price_ = ask_px
        self._ask_size_ = ask_sz
    



class SecurityMarketView:
    #variables
    market_update_info
    trade_print_info
    l1_price_listeners
    
    
    
    def __init_(self. watch, shortcode, exchange_symbol, security_id):
    
    
    #===========================================================================
    # 
    # def __init__(self, bid_price, bid_size, ask_price, ask_size, min_price_increment):
    #     #initialisation
    #     self._bid_price_ = bid_price
    #     self._bid_size_ = bid_size
    #     self._ask_price_ = ask_price
    #     self._ask_size_ = ask_size
    #     self._min_price_increment = min_price_increment
    #     self._mkt_price = (bid_price * ask_size + ask_price * bid_size )/ (bid_size + ask_size )
    #     
    #     
    #===========================================================================
        
        
        
        
        
    def isL1Valid(self):
        return
    
    
    
    
        
    def GetPriceFromType(self, price_type, market_update_info):
        return 
        
    def get_min_price_increment(self):
        return self._min_price_increment
    
    def get_bid_price(self):
        return self._bid_price_
    
    def get_bid_size(self):
        return self._bid_size_
    
    def get_ask_price(self):
        return self._ask_price_
    
    def get_ask_size(self):
        return self._ask_size_
    
    def compute_mkt_price(self):
        self._mkt_price = (self._bid_price_ * self._ask_size_ + self._ask_price_ * self._bid_size_ ) / (self._ask_size_ + self._bid_size_)
        
    def get_mkt_price(self):
        self.compute_mkt_price()
        return self._mkt_price
    
    def update_l1_bid(self):
        #compute mkt px
        #update
        return
        
    def update(self):
        #compute mkt px
        return
        
    def onMarketUpdate(self):
        ##
        return
        
    def OnTradeUpdate(self):
        ##
        return
        
    def subscribe_l1_update(self, smv_listener):
        return
    
    

    