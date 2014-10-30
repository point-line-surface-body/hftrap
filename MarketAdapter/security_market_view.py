from CommonTradeUtils.security_definitions import SecurityDefinitions
from abc import ABCMeta
from abc import abstractmethod

class TradePrintInfo():
    
    def __init__(self):
        self.buysell_ = 'B'
        self.trade_price_ = 0.0
        self.size_traded_ = 0
        self.int_trade_price_ = 0
        
    def Dump(self):
        print('['+self.buysell_+' '+str(self.size_traded_)+' '+str(self.int_trade_price_)+']')
    
class MarketUpdateInfo():
    def __init__(self, _shortcode_):
        self.shortcode_ = _shortcode_
        self.bestbid_price_ = 0
        self.bestbid_size_ = 0
        self.bestbid_int_price_ = 0
        self.bestbid_ordercount_ = 0
        self.bestask_price_ = 0
        self.bestask_size_ = 0
        self.bestask_int_price_ = 0
        self.bestask_ordercount_ = 0
        self.spread_increments_ = 1
        self.mkt_size_weighted_price_ = 0
    
    def Dump(self):
        print('['+str(self.bestbid_size_)+' '+str(self.bestbid_int_price_)+' | '+str(self.bestask_int_price_)+' '
              +str(self.bestask_size_)+']')
        
class SecurityMarketViewOnReadyListener:
    __metaclass__ = ABCMeta
    @abstractmethod
    def SMVOnReady(self):
        return
    
class SecurityMarketViewChangeListener():
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def OnMarketUpdate(self, _market_update_info_):
        return
    
    @abstractmethod
    def OnTradePrint(self, _trade_print_info_, _market_update_info_):
        return


class SecurityMarketView:

    def __init__(self, _watch_, _shortcode_):
        self.shortcode_ = _shortcode_
        self.watch_ = _watch_
        self.min_price_increment_ = SecurityDefinitions.GetContractMinPriceIncrement(_shortcode_, self.watch_.TradingDate())
        self.min_order_size_ = 1
        self.is_ready_ = False
        self.market_update_info_ = MarketUpdateInfo(_shortcode_)
        self.trade_print_info_ = TradePrintInfo()
        self.l1_price_listeners_ = []
        self.is_ready_ = False
        self.market_update_info_ = MarketUpdateInfo(_shortcode_)
        self.trade_print_info_ = TradePrintInfo()
        self.l1_price_listeners_ = []
        self.onready_listeners_ = []
        self.price_type_subscribed_ = {}
        self.count_ = 0
        self.sim_market_maker_ = None
        self.price_type_subscribed_['MktSizeWPrice'] = False
    
    def SetSimMarketMaker(self, _sim_market_maker_):
        self.sim_market_maker_ = _sim_market_maker_
      
    def __eq__(self, _obj_):
        return self.shortcode() == _obj_.shortcode()
    
    def shortcode(self):
        return self.market_update_info_.shortcode_
    
    def bestbid_price(self):
        return self.market_update_info_.bestbid_price_
        
    def bestask_price(self):
        return self.market_update_info_.bestask_price_
        
    def bestbid_int_price(self):
        return self.market_update_info_.bestbid_int_price_
      
    def bestask_int_price(self):
        return self.market_update_info_.bestask_int_price_
        
    def bestbid_size(self):
        return self.market_update_info_.bestbid_size_
        
    def bestask_size(self):
        return self.market_update_info_.bestask_size_
        
    def spread_increments(self):
        return self.market_update_info_.bestask_int_price_ - self.market_update_info_.bestbid_int_price_

    def MinPriceIncrement(self):
        return self.min_price_increment_
    
    def MinOrderSize(self):
        return self.min_order_size_
    
    def SubscribePriceType(self, _new_listener_, _price_type_):
        if _price_type_ == 'MktSizeWPrice':
            self.price_type_subscribed_[_price_type_] = True
            if _new_listener_ is not None:
                self.SubscribeL1Only(_new_listener_)
            return True
        else:
            return False
    
    def SubscribeL1Only(self, _new_listener_):
        if not self.l1_price_listeners_.__contains__(_new_listener_):
            #print('********Added Listener********')
            self.l1_price_listeners_.append(_new_listener_)
        
    def SubscribeOnReady(self, _new_listener_):
        if not self.onready_listeners_.__contains__(_new_listener_):
            self.onready_listeners_.append(_new_listener_)
       
    def UpdateL1Prices(self):
        self.market_update_info_.mkt_size_weighted_price_ = (self.market_update_info_.bestbid_price_ * self.market_update_info_.bestask_size_ + self.market_update_info_.bestask_price_ * self.market_update_info_.bestbid_size_) / (self.market_update_info_.bestbid_size_ + self.market_update_info_.bestask_size_)

    def NotifyL1PriceListeners(self):
        #print('NotifyL1PriceListeners')
        #print(self.is_ready_)
        if not self.is_ready_:
            return
        #if self.using_order_level_data_ and self.watch_.tv() <= self.skip_listener_notification_end_time_:
        #    return
        for i in range(len(self.l1_price_listeners_)):
            self.l1_price_listeners_[i].OnMarketUpdate(self.market_update_info_)
        #self.market_update_info_.l1events_ += 1
    
    def NotifyOnReadyListeners(self):
        if not self.is_ready_: 
            return 
        #if self.using_order_level_data_ and self.watch_.tv() <= self.skip_listener_notification_end_time_:
        #    return
        for i in range(len(self.onready_listeners_)):
            self.onready_listeners_[i].SMVOnReady()
            
    def NotifyTradeListeners(self):
        for x in self.l1_price_listeners_:
            x.OnTradePrint(self.trade_print_info_, self.market_update_info_)
        return
    
    def GetMidPrice(self):
        return (self.bestask_price() + self.bestbid_price()) * 0.5
    
    def GetMidIntPrice(self):
        return (self.bestask_int_price() + self.bestbid_int_price()) * 0.5
    
    def GetPriceFromType(self, _price_type_):
        if _price_type_ == 'MktSizeWPrice':
            return self.market_update_info_.mkt_size_weighted_price_
        elif _price_type_ == 'AskPrice':
            return self.market_update_info_.bestask_price_
        elif _price_type_ == 'BidPrice':
            return self.market_update_info_.bestbid_price_
        else:
            return self.market_update_info_.mkt_size_weighted_price_
    
    def OnTradePrint(self, _trade_price_, _trade_size_, _trade_type_, 
                bid_int_price_, bid_size_, bid_order_count_, ask_int_price_, ask_size_, ask_order_count_):
        self.trade_print_info_.buysell_ = _trade_type_
        self.trade_print_info_.trade_price_ = float(_trade_price_) * self.MinPriceIncrement()
        self.trade_print_info_.size_traded_ = _trade_size_
        self.trade_print_info_.int_trade_price_ = _trade_price_
        ask_price = float(ask_int_price_) * self.MinPriceIncrement()
        bid_price_ = float(bid_int_price_) * self.MinPriceIncrement()
        self.market_update_info_.bestask_price_ = ask_price
        self.market_update_info_.bestask_size_ = ask_size_
        self.market_update_info_.bestask_int_price_ = ask_int_price_
        self.market_update_info_.bestask_ordercount_ = ask_order_count_
        self.market_update_info_.bestbid_price_ = bid_price_
        self.market_update_info_.bestbid_size_ = bid_size_
        self.market_update_info_.bestbid_int_price_ = bid_int_price_
        self.market_update_info_.bestbid_ordercount_ = bid_order_count_
        self.market_update_info_.spread_increments_ = ask_int_price_ - bid_int_price_

        self.count_ += 1
        self.UpdateL1Prices()
        print('---------------------------------------------------------------------------------------')
        #print 'SMV.OnTradePrint: '+str(self.count_)
        self.trade_print_info_.Dump()
        self.market_update_info_.Dump()
        self.is_ready_ = True
        self.NotifyL1PriceListeners()
        #self.NotifyTradeListeners()
        if (self.sim_market_maker_ is not None):
            self.sim_market_maker_.OnTradePrint(self.trade_print_info_, self.market_update_info_)
        self.NotifyOnReadyListeners()
        #print('---------------------------------------------------------------------------------------')
        #if (self.count_ == 10):
        #    exit()
        #print('trade_before_quote:'),
        #print(self.trade_before_quote_)
        #if self.trade_before_quote_:
        #if self.trade_print_info_.buysell_ == 'B':
        #    self.SetBestLevelAskVariablesOnLift()
        #else:
        #    self.SetBestLevelBidVariablesOnHit()
        #if self.is_ready_:
#         self.NotifyTradeListeners()
#         self.NotifyOnReadyListeners()
        
        #else:
        #    if self.is_ready_:
        #        self.UpdateL1Prices()
        #        self.NotifyTradeListeners()
        #        self.NotifyOnReadyListeners()
        #else:
        #    self.NotifyTradeListeners()
        #    self.NotifyOnReadyListeners()
        #self.NotifyTradeListeners()


    def trade_before_quote(self):
        return False

    def OnMarketUpdate(self, bid_int_price_, bid_size_, bid_order_count_, ask_int_price_, ask_size_, ask_order_count_):
        #print('SMV.OnMarketUpdate')
        #print self.bestask_price(), self.market_update_info_.bestask_price_

        #self.top_ask_level_to_mask_trades_on_ = 0
        #self.top_bid_level_to_mask_trades_on_ = 0
        ask_price = float(ask_int_price_) * self.MinPriceIncrement()
        bid_price_ = float(bid_int_price_) * self.MinPriceIncrement()
        #while ask_int_price_ > self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_ ].limit_int_price_ and self.top_ask_level_to_mask_trades_on_ < min( DEF_MARKET_DEPTH - 1, len(self.market_update_info_.asklevels_) - 1 ) : 
        #    self.top_ask_level_to_mask_trades_on_ += 1
        #while bid_int_price_ < self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_ ].limit_int_price_ and self.top_bid_level_to_mask_trades_on_ < min( DEF_MARKET_DEPTH - 1, len(self.market_update_info_.bidlevels_) - 1 ) :
        #    self.top_bid_level_to_mask_trades_on_ += 1
        self.market_update_info_.bestask_price_ = ask_price
        self.market_update_info_.bestask_size_ = ask_size_
        self.market_update_info_.bestask_int_price_ = ask_int_price_
        self.market_update_info_.bestask_ordercount_ = ask_order_count_
        self.market_update_info_.bestbid_price_ = bid_price_
        self.market_update_info_.bestbid_size_ = bid_size_
        self.market_update_info_.bestbid_int_price_ = bid_int_price_
        self.market_update_info_.bestbid_ordercount_ = bid_order_count_
        self.market_update_info_.spread_increments_ = ask_int_price_ - bid_int_price_
        self.UpdateL1Prices()

        if (self.count_ == 0):
            print 'Listeners of SMV:'
            print self.l1_price_listeners_
            print self.onready_listeners_
            
        print('---------------------------------------------------------------------------------------')
        print (self.count_+1),
        self.market_update_info_.Dump()
        #self.OnL1PriceUpdate()
        
        self.count_ += 1
        #print 'SMV.OnMarketUpdate: '+str(self.count_)
        self.is_ready_ = True
        self.NotifyL1PriceListeners()
        if (self.sim_market_maker_ is not None):
            self.sim_market_maker_.OnMarketUpdate(self.market_update_info_)
        self.NotifyOnReadyListeners()
        #print('---------------------------------------------------------------------------------------')

        #if (self.count_ == 10):
        #    exit()
        
        #print self.bestask_price(), self.market_update_info_.bestask_price_
        #print self.bestask_price(), self.market_update_info_.bestask_price_
