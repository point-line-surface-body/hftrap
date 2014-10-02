from CDef.defines import *


#Keeping only 1 Level in the book
class OrderBook():
    
    def __init__(self, bid_px, bid_sz, ask_px, ask_sz):
        self._bid_price_ = bid_px
        self._bid_size_ = bid_sz
        self._ask_price_ = ask_px
        self._ask_size_ = ask_sz
    
class PriceLevelInfo():
    def __init__(self, *argv):
        if len(argv) == 3 :
            self.limit_price_ = (float)(argv[0])
            self. limit_size_ = (int)(argv[1])
            self.limit_ordercount_ = (int)(argv[2])
        else :
            self.limit_price_ = 0.0
            self. limit_size_ = 0
            self.limit_ordercount_ = 0


class SecurityMarketView:
    #variables
    market_update_info
    trade_print_info
    l1_price_listeners = []
    l1_size_listeners = []
    onready_listeners_ = []
    price_type_subscribed = dict()
    min_price_increment_
    min_order_size_
    normal_spread_increments_
    normal_spread_
    is_ready_
    
    
    def __init_(self, watch, shortcode, exchange_symbol, security_id):
        return
    
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
        
    #def __eq__(self):
        
        
    def subscribe_price_type (self, t_new_listener_, t_price_type_ ) :
        res = True
        if t_price_type_ == "MktSizeWPrice":
            self.price_type_subscribed[t_price_type_] = True
            if t_new_listener_ is not None :
                if not self.l1_price_listeners.__contains__(t_new_listener_) :
                    self.l1_price_listeners.append(t_new_listener_)
                if not self.l1_size_listeners.__contains__(t_new_listener_) :
                    self.l1_size_listeners.append(t_new_listener_)
        else :
            res = False
        return res
    
    def subscribe_L1_Only(self,t_new_listener_ ):
        if not self.l1_price_listeners.__contains__(t_new_listener_) :
            self.l1_price_listeners.append(t_new_listener_)
        if not self.l1_size_listeners.__contains__(t_new_listener_) :
            self.l1_size_listeners.append(t_new_listener_)
        
    def subscribe_OnReady(self, t_new_listener_):
        if not self.onready_listeners_.__contains__(t_new_listener_) :
            self.onready_listeners_.append(t_new_listener_)
        
    def OnL1PriceUpdate(self):
        self.UpdateL1Prices()
        self.NotifyL1PriceListeners()
        self.NotifyOnReadyListeners()
       
    def UpdateL1Prices(self):
        self.market_update_info_.mkt_size_weighted_price_ = ( self.market_update_info_.bestbid_price_ * self.market_update_info_.bestask_size_ + self.market_update_info_.bestask_price_ * self.market_update_info_.bestbid_size_ ) / ( self.market_update_info_.bestbid_size_ + self.market_update_info_.bestask_size_ ) ;

    def OnL1SizeUpdate(self):
        return

    def NotifyL1PriceListeners(self):
        return
    
    def NotifyOnReadyListeners(self):
        return
    
    def OnL1Trade (self, trade_price, trade_size, trade_type):
        return
    
    def OnTrade (self, trade_price, trade_size, trade_type):
        return
    
    def Uncross(self):
        return
    
    def ShowMarket(self):
        return
    
    def isL1Valid(self):
        return
    
    
    
    
        
    #===========================================================================
    # def GetPriceFromType(self, price_type, market_update_info):
    #     return 
    #     
    # def get_min_price_increment(self):
    #     return self._min_price_increment
    # 
    # def get_bid_price(self):
    #     return self._bid_price_
    # 
    # def get_bid_size(self):
    #     return self._bid_size_
    # 
    # def get_ask_price(self):
    #     return self._ask_price_
    # 
    # def get_ask_size(self):
    #     return self._ask_size_
    # 
    # def compute_mkt_price(self):
    #     self._mkt_price = (self._bid_price_ * self._ask_size_ + self._ask_price_ * self._bid_size_ ) / (self._ask_size_ + self._bid_size_)
    #     
    # def get_mkt_price(self):
    #     self.compute_mkt_price()
    #     return self._mkt_price
    # 
    # def update_l1_bid(self):
    #     #compute mkt px
    #     #update
    #     return
    #     
    # def update(self):
    #     #compute mkt px
    #     return
    #     
    # def onMarketUpdate(self):
    #     ##
    #     return
    #     
    # def OnTradeUpdate(self):
    #     ##
    #     return
    #     
    # def subscribe_l1_update(self, smv_listener):
    #     return
    #===========================================================================
    
    

    