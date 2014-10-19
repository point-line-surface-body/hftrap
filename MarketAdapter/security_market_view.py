from CDef.security_definitions import SecurityDefinitions
from MarketAdapter.basic_market_view import MarketUpdateInfo, TradePrintInfo

# #Keeping only 1 Level in the book
# class OrderBook():  
#     def __init__(self, bid_px, bid_sz, ask_px, ask_sz):
#         self._bid_price_ = bid_px
#         self._bid_size_ = bid_sz
#         self._ask_price_ = ask_px
#         self._ask_size_ = ask_sz
# 
# class PriceLevelInfo():
#     def __init__(self, *argv):
#         if len(argv) == 3:
#             self.limit_price_ = (float)(argv[0])
#             self.limit_size_ = (int)(argv[1])
#             self.limit_ordercount_ = (int)(argv[2])
#         else:
#             self.limit_price_ = 0.0
#             self.limit_size_ = 0
#             self.limit_ordercount_ = 0

class SecurityMarketView:

    def __init__(self, _watch_, _shortcode_, _security_id_):
        self.watch_ = _watch_
        self.min_price_increment_ = SecurityDefinitions.GetContractMinPriceIncrement(_shortcode_, self.watch_.TradingDate())
        self.min_order_size_ = SecurityDefinitions.GetContractMinOrderSize(_shortcode_, self.watch_.TradingDate())
#        self.normal_spread_ = 1 * self.min_price_increment_
        self.is_ready_ = False
#        self.computing_price_levels_ = False
#        self.trade_before_quote_ = SecurityDefinitions.GetTradeBeforeQuote(_shortcode_, self.watch_.TradingDate())
        self.market_update_info_ = MarketUpdateInfo(_shortcode_, _security_id_, SecurityDefinitions.GetContractExchSource(_shortcode_, self.watch_.TradingDate()))
        self.trade_print_info_ = TradePrintInfo()
        self.l1_price_listeners_ = []
#        self.l1_size_listeners_ = []
        self.onready_listeners_ = []
        self.price_type_subscribed_ = {}
        self.count_ = 0
#         self.use_order_level_book_ = False
#         #following variables may not be needed
#         self.conf_to_market_update_msecs_ = SecurityDefinitions.GetConfToMarketUpdateMsecs(_shortcode_, self.watch_.TradingDate())
#         self.self_best_bid_ask_ = BestBidAskInfo()
#         self.last_best_level_ = BestBidAskInfo()
#         self.current_best_level_ = BestBidAskInfo()
#         self.top_bid_level_to_mask_trades_on_ = 0
#         self.top_ask_level_to_mask_trades_on_ = 0
#         self.prev_bid_was_quote_ = True
#         self.prev_ask_was_quote_ = True
#         self.running_hit_size_vec_ = []
#         self.running_lift_size_vec_ = []
#         self.l1_changed_since_last_ = False
#         self.last_message_was_trade_ = False
#         self.min_priority_size_ = 10
#         self.max_priority_size_ = 500
#         self.suspect_book_correct_ = False
#         self.using_order_level_data_ = False
#         self.skip_listener_notification_end_time_ = 0.0
#         self.process_market_data_ = True
#         self.initial_book_constructed_ = False
#         self.int_price_bid_book_ = []
#         self.int_price_ask_book_ = []
#         self.int_price_bid_skip_delete_ = []
#         self.int_price_ask_skip_delete_ = []
#         self.indexed_bid_book_ = []
#         self.indexed_ask_book_ = []
#         self.base_bid_index_ = 0
#         self.base_ask_index_ = 0
#         self.last_base_bid_index_ = 0
#         self.last_base_ask_index_ = 0
#         self.this_int_price_ = 0
#         self.last_msg_was_quote_ = False
#         self.running_lift_size_ = 0
#         self.running_hit_size_ = 0
#         self.lift_base_index_ = 0
#         self.hit_base_index_ = 0
#        self.last_raw_message_sequence_applied_ = 0
        self.price_type_subscribed_['MktSizeWPrice'] = False
#         self.running_hit_size_vec_ = []
#         self.running_lift_size_vec_ = []
#         i=0
#         while i < DEF_MARKET_DEPTH :
#             self.running_hit_size_vec_.append(0)
#             self.running_lift_size_vec_.append(0)
#             i = i+1
      
    def __eq__(self, _obj_):
        return self.shortcode() == _obj_.shortcode()
    
    def shortcode(self):
        return self.market_update_info_.shortcode_
    
#    def secname(self):
#        return self.market_update_info_.secname_
    
#     def security_id(self):
#         return self.market_update_info_.security_id_

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
    
#     def UseOrderLevelBook(self):
#         return self.use_order_level_book_
#     
#     def SetUseOrderLevelBook(self):
#         self.use_order_level_book_ = True
#         
#     def UnsetUseOrderLevelBook(self):
#         self.use_order_level_book_ = False
            
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
#         if not self.l1_size_listeners_.__contains__(_new_listener_):
#             self.l1_size_listeners_.append(_new_listener_)
#         print(len(self.l1_price_listeners_))
#         print(self.l1_price_listeners_)
        
    def SubscribeOnReady(self, _new_listener_):
        if not self.onready_listeners_.__contains__(_new_listener_):
            self.onready_listeners_.append(_new_listener_)
#         
#     def OnL1PriceUpdate(self):
#         self.UpdateL1Prices()
#         self.is_ready_ = True
#         self.NotifyL1PriceListeners()
#         self.NotifyOnReadyListeners()
       
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
            
#     def StorePreTrade(self):
#         if self.market_update_info_.storing_pretrade_state_:
#             self.market_update_info_.pretrade_bestbid_price_ = self.market_update_info_.bestbid_price_
#             self.market_update_info_.pretrade_bestbid_int_price_ = self.market_update_info_.bestbid_int_price_
#             self.market_update_info_.pretrade_bestbid_size_ = self.market_update_info_.bestbid_size_
#             self.market_update_info_.pretrade_bestask_price_ = self.market_update_info_.bestask_price_
#             self.market_update_info_.pretrade_bestask_int_price_ = self.market_update_info_.bestask_int_price_
#             self.market_update_info_.pretrade_bestask_size_ = self.market_update_info_.bestask_size_
#             self.market_update_info_.pretrade_mid_price_ = self.market_update_info_.mid_price_    
#                     
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
        #if self.trade_print_info_.computing_last_book_tdiff_ and self.prev_bid_was_quote_ and self.prev_ask_was_quote_:
        #    self.market_update_info_.last_book_mkt_size_weighted_price_ = self.market_update_info_.mkt_size_weighted_price_
        #if not self.market_update_info_.trade_update_implied_quote_:
        #    self.market_update_info_.trade_update_implied_quote_ = True
        #self.StorePreTrade()
        self.trade_print_info_.buysell_ = _trade_type_
        self.trade_print_info_.trade_price_ = _trade_price_
        self.trade_print_info_.size_traded_ = _trade_size_
        self.trade_print_info_.int_trade_price_ = float(_trade_price_) * self.MinPriceIncrement()

        ask_price = float(ask_int_price_) * self.MinPriceIncrement()
        bid_price_ = float(bid_int_price_) * self.MinPriceIncrement()
        self.market_update_info_.bestask_price_ = ask_price
        self.market_update_info_.bestask_size_ = ask_size_
        self.market_update_info_.bestask_int_price_ = ask_int_price_
        self.market_update_info_.bestask_ordercount_ = ask_order_count_
        self.market_update_info_.bestbid_price_ = bid_price_
        self.market_update_info_.bestbid_size_ = bid_size_
        self.market_update_info_.bestbid_int_price_ = bid_int_price_
        self.market_update_info_.bestask_ordercount_ = bid_order_count_
        
        self.count_ += 1
        self.UpdateL1Prices()
        self.is_ready_ = True
        self.NotifyL1PriceListeners()
        self.NotifyTradeListeners()
        self.NotifyOnReadyListeners()
        if (self.count_ == 10):
            exit()
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

 
#     def Uncross(self):
#         res = False
#         if self.IsL1Valid():
#             while self.market_update_info_.bidlevels_[0].limit_int_price_ >= self.market_update_info_.asklevels_[0].limit_int_price_:
#                 res = True
#                 if self.market_update_info_.asklevels_[0].mod_time_ < self.market_update_info_.bidlevels_[0].mod_time_:
#                     self.RemoveTopAsk()
#                 else:
#                     self.RemoveTopBid()
#         return res
#         
#     def RemoveTopAsk(self):
#         if len (self.market_update_info_.asklevels_) > 0:
#             del self.market_update_info_.asklevels_[0]            
#  
#     def RemoveTopBid(self):
#         if len (self.market_update_info_.bidlevels_) > 0:
#             del self.market_update_info_.bidlevels_[0]
#                
#     def IsL1Valid(self):
#         return  len(self.market_update_info_.bidlevels_) > 0 and len(self.market_update_info_.asklevels_) > 0

#     def ShowMarket(self):
#         res =  self.market_update_info_.secname_ + " " + str(self.market_update_info_.bidlevels_[0].limit_int_price_level_) + " " + str(self.market_update_info_.bidlevels_[0].limit_size_)
#         res += " " + str(self.market_update_info_.bidlevels_[0].limit_ordercount_) + " " + str(self.market_update_info_.bidlevels_[0].limit_price_) +  " " + str(self.market_update_info_.bidlevels_[0].limit_int_price_)
#         res += " X " + str(self.market_update_info_.asklevels_[0].limit_int_price_)+ " " + str(self.market_update_info_.asklevels_[0].limit_price_) + " " + str(self.market_update_info_.asklevels_[0].limit_ordercount_)
#         res += " " +  str(self.market_update_info_.asklevels_[0].limit_size_)  + " " + self.market_update_info_.asklevels_[0].limit_int_price_level_
#         return res 

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
        self.market_update_info_.bestask_ordercount_ = bid_order_count_
        #print 'Listeners of SMV:'
        #print self.l1_price_listeners_
        #print self.onready_listeners_
        #self.OnL1PriceUpdate()
        
        self.count_ += 1
        print 'SMV.OnMarketUpdate: '+str(self.count_)
        self.UpdateL1Prices()
        self.is_ready_ = True
        self.NotifyL1PriceListeners()
        self.NotifyOnReadyListeners()
        if (self.count_ == 10):
            exit()
        
        #print self.bestask_price(), self.market_update_info_.bestask_price_
'''     
    def SetBestLevelAskVariablesOnLift(self):
        if self.prev_ask_was_quote_ :
            for i in range (len(self.running_lift_size_vec_)):
                self.running_lift_size_vec_[i] = 0
                self.prev_ask_was_quote_ = False
                self.top_ask_level_to_mask_trades_on_ = 0
        if len(self.market_update_info_.asklevels_) ==0 :
            return 
        while self.trade_print_info_.int_trade_price_ > self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_ ].limit_int_price_ and self.top_ask_level_to_mask_trades_on_ < min( DEF_MARKET_DEPTH - 1, len(self.market_update_info_.asklevels_) - 1 ) : 
            self.top_ask_level_to_mask_trades_on_ += 1
        if self.trade_print_info_.int_trade_price_ == self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_int_price_ :
            self.running_lift_size_vec_[self.top_ask_level_to_mask_trades_on_] += self.trade_print_info_.size_traded_
            t_trade_masked_best_ask_size_ = self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_size_ - self.running_lift_size_vec_[self.top_ask_level_to_mask_trades_on_] 
            if t_trade_masked_best_ask_size_ <= 0 :
                if self.top_ask_level_to_mask_trades_on_ < min( DEF_MARKET_DEPTH - 1, len(self.market_update_info_.asklevels_) - 1 ) :
                    self.top_ask_level_to_mask_trades_on_ += 1
                    self.market_update_info_.bestask_price_ = self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_price_
                    self.market_update_info_.bestask_size_ =self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_size_
                    self.market_update_info_.bestask_int_price_ = self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_int_price_
                    self.market_update_info_.bestask_ordercount_ = self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_ordercount_
                else :
                    self.market_update_info_.bestask_price_ = self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_price_
                    self.market_update_info_.bestask_size_ = 1
                    self.market_update_info_.bestask_int_price_ = self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_int_price_
                    self.market_update_info_.bestask_ordercount_ = self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_ordercount_
            else :
                self.market_update_info_.bestask_price_ = self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_price_
                self.market_update_info_.bestask_size_ = t_trade_masked_best_ask_size_
                self.market_update_info_.bestask_int_price_ = self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_int_price_
                self.market_update_info_.bestask_ordercount_ = self.market_update_info_.asklevels_[self.top_ask_level_to_mask_trades_on_].limit_ordercount_

    def SetBestLevelBidVariablesOnHit(self):
        if self.prev_bid_was_quote_ :
            for i in range (len(self.running_hit_size_vec_)):
                self.running_hit_size_vec_[i] = 0
                self.prev_bid_was_quote_ = False
                self.top_bid_level_to_mask_trades_on_ = 0
        if len(self.market_update_info_.bidlevels_) ==0 :
            return
        while self.trade_print_info_.int_trade_price_ < self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_ ].limit_int_price_ and self.top_bid_level_to_mask_trades_on_ < min( DEF_MARKET_DEPTH - 1, len(self.market_update_info_.bidlevels_) - 1 ) :
            self.top_bid_level_to_mask_trades_on_ += 1
        if self.trade_print_info_.int_trade_price_ == self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_int_price_ :
            self.running_hit_size_vec_[self.top_bid_level_to_mask_trades_on_] += self.trade_print_info_.size_traded_
            t_trade_masked_best_bid_size_ = self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_size_ - self.running_hit_size_vec_[self.top_bid_level_to_mask_trades_on_] 
            if t_trade_masked_best_bid_size_ <= 0 :
                if self.top_bid_level_to_mask_trades_on_ < min( DEF_MARKET_DEPTH - 1, len(self.market_update_info_.bidlevels_) - 1 ) :
                    self.top_bid_level_to_mask_trades_on_ += 1
                    self.market_update_info_.bestbid_price_ = self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_price_
                    self.market_update_info_.bestbid_size_ =self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_size_
                    self.market_update_info_.bestbid_int_price_ = self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_int_price_
                    self.market_update_info_.bestbid_ordercount_ = self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_ordercount_
                else :
                    self.market_update_info_.bestbid_price_ = self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_price_
                    self.market_update_info_.bestbid_size_ = 1
                    self.market_update_info_.bestbid_int_price_ = self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_int_price_
                    self.market_update_info_.bestbid_ordercount_ = self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_ordercount_
            else :
                self.market_update_info_.bestbid_price_ = self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_price_
                self.market_update_info_.bestbid_size_ = t_trade_masked_best_bid_size_
                self.market_update_info_.bestbid_int_price_ = self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_int_price_
                self.market_update_info_.bestbid_ordercount_ = self.market_update_info_.bidlevels_[self.top_bid_level_to_mask_trades_on_].limit_ordercount_
'''
        