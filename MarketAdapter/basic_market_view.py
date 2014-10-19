from CDef.defines import MAX_LEVELS, kInvalidIntPrice, kInvalidPrice

class TradePrintInfo():
    
    def __init__(self):
        self.buysell_ = "NOTRADETYPE" # B S
        self.trade_price_ =0.0
        self.size_traded_ = 0
        self.int_trade_price_ = 0.0
#         self.computing_trade_impact_ = False
#         self.trade_impact_ = 0.0
#         self.computing_int_trade_type_ = False
#         self.int_trade_type_ = 0
#         self.computing_sqrt_size_traded_ = False
#         self.sqrt_size_traded_=  0.0
#         self.computing_sqrt_trade_impact_ = False
#         self.sqrt_trade_impact_ = 0.0
#         self.computing_tradepx_mktpx_diff_ = False
#         self.tradepx_mktpx_diff_ = 0.0
#         self.computing_last_book_tdiff_ = False
#         self.last_book_tdiff_ = 0.0
#         self.num_trades_ = 0

#     def ToString(self):
#         res = "[ " + self.buysell_ + " " + self.size_traded_ + " @ " + str(self.trade_price_) + " ] " 
#         return res

# class BestBidAskInfo():
#     def __init__(self, *argv):
#         
#         self.best_bid_price_ = 0.0
#         self.best_ask_price_ =0.0
#         self.best_bid_size_ = 0
#         self.best_ask_size_ = 0
#         self.best_bid_orders_ = 0
#         self.best_ask_orders_ = 0
#         self.msecs_from_midnight_ = 0
#         
#         if len(argv) >=6 :
#             self.best_bid_price_ = (float)(argv[0])
#             self.best_ask_price_ = (float)(argv[1])
#             self.best_bid_size_ = (int)(argv[2])
#             self.best_ask_size_ = (int)(argv[3])
#             self.best_bid_orders_ = (int)(argv[4])
#             self.best_ask_orders_ = (int)(argv[5])
#             if len(argv) >=7 :
#                 self.msecs_from_midnight_ = (int)(argv[6])
#         if len(argv) == 1:
#             if len(argv[0].bidlevels_) >=1 : 
#                 self.best_bid_price_ = argv[0].bidlevels_[0].limit_int_price_
#                 self.best_bid_size_ = argv[0].bidlevels_[0].limit_size_
#                 self.best_bid_orders_ = argv[0].bidlevels_[0].limit_ordercount_
#             else :
#                 self.best_bid_price_ = 0.0
#                 self.best_bid_size_ = 0
#                 self.best_bid_orders_ = 0
#             if len(argv[0].asklevels_) >=1 :
#                 self.best_ask_price_ = argv[0].asklevels_[0].limit_int_price_
#                 self.best_ask_size_ = argv[0].asklevels_[0].limit_size_
#                 self.best_ask_orders_ = argv[0].asklevels_[0].limit_ordercount_
#             else:
#                 self.best_ask_price_ = 0.0
#                 self.best_ask_size_ = 0
#                 self.best_ask_orders_ = 0
# 
#     def ToString(self):
#         res = " " + str(self.msecs_from_midnight_) + " " + str(self.best_bid_size_) + " " + str(self.best_bid_orders_) + " " + str(self.best_bid_price_) + " X " + str(self.best_ask_price_) + " " + str(self.best_ask_size_) + " " + str(self.best_ask_orders_)
#         return res
#     
#     def __eq__(self,obj ):
#         is_equal_ = False
#         if self.best_bid_price_ == obj.best_bid_price_ and self.best_bid_size_ == obj.best_bid_size_ and self.best_bid_orders_ == obj.best_bid_orders_ and self.best_ask_price_ == obj.best_ask_price_ and self.best_ask_size_ == obj.best_ask_size_ and self.best_ask_orders_ == obj.best_ask_orders_ : 
#             is_equal_ = True
#         return is_equal_
#     
#     def __sub__(self, obj):
#         diff = self
#         if self.best_bid_price_ == obj.best_bid_price_ :
#             diff.best_bid_price_ = self.best_bid_price_
#             diff.best_bid_size_ = self.best_bid_size_ - obj.best_bid_size_
#             diff.best_bid_orders_ = self.best_bid_orders_ - obj.best_bid_orders_
#         if self.best_ask_price_ == obj.best_ask_price_ :
#             diff.best_ask_price_ = self.best_ask_price_
#             diff.best_ask_size_ = self.best_ask_size_ - obj.best_ask_size_
#             diff.best_ask_orders_ = self.best_ask_orders_ - obj.best_ask_orders_
#         return diff
#     
#     def __add__(self, obj):
#         res = self
#         if self.best_bid_price_ == obj.best_bid_price_:
#             res.best_bid_price_ = self.best_bid_price_
#             res.best_bid_size_ = self.best_bid_size_ + obj.best_bid_size_
#             res.best_bid_orders_ = self.best_bid_orders_ + obj.best_bid_orders_
#         elif self.best_bid_price_ < obj.best_bid_price_ :
#             res.best_bid_price_ = obj.best_bid_price_
#             res.best_bid_size_ = obj.best_bid_size_
#             res.best_bid_orders_ = obj.best_bid_orders_
#         
#         if self.best_ask_price_ == obj.best_ask_price_ :
#             res.best_ask_price_ = self.best_ask_price_
#             res.best_ask_size_ = self.best_ask_size_ + obj.best_ask_size_
#             res.best_ask_orders_ = self.best_ask_orders_ + obj.best_ask_orders_
#         elif self.best_ask_price_ > obj.best_ask_price_ :
#             res.best_ask_price_ = obj.best_ask_price_
#             res.best_ask_size_ = obj.best_ask_size_
#             res.best_ask_orders_ = obj.best_ask_orders_
#         return res
#   
#     
# class MarketUpdateInfoLevelStruct():
#     #int priority_size_filled_ ;
#     def __init__(self, *argv):
#         
#         self.limit_int_price_level_= MAX_LEVELS
#         self.limit_int_price_  = kInvalidIntPrice
#         self.limit_price_ = kInvalidPrice
#         self.limit_size_ = 0
#         self.limit_ordercount_ = 0
#         self.mod_time_  =  0.0 
#         self.priority_size_ = 0 ;
#         if len(argv) >= 6 :
#             self.limit_int_price_level_ = (int)(argv[0])
#             self.limit_int_price_  = (int)(argv[1])
#             self.limit_price_ = (float)(argv[2])
#             self.limit_size_ = (int)(argv[3])
#             self.limit_ordercount_ =(float)(argv[4])
#             if isinstance(argv[5], int):
#                 self.priority_size_ = (int)(argv[5])
#             else:
#                 self.mod_time_ = (float)(argv[5])
#                 if len(argv) == 7:
#                     self.priority_size_ = (int)(argv[6])
#    
#     def InValidateLevel(self):
#         self.limit_int_price_level_= MAX_LEVELS
#         self.limit_int_price_  = kInvalidIntPrice
#         self.limit_price_ = kInvalidPrice
#         self.limit_size_ = 0
#         self.limit_ordercount_ = -1
#         self.mod_time_  =  0.0 
#         self.priority_size_ = 0 ;
#           
#     def GetPriceAsStr(self):
#         return str(self.limit_price_)
#     
#       
# class MarketOrder():
#     
#     def __init__(self, *argv):
#         if len(argv) ==0 :
#             return
#         self.int_price_ = (int) (argv[0])
#         self.size_ = (int)(argv[1])
#         self.order_count_= (int)(argv[2])
#         self.level_ = (int)(argv[3])
#         self.order_entry_time_ = (float)(argv[4])
#         self.priority_ = False
#         if len(argv) == 6 :
#             self.priority_ = (bool)(argv[5])
#     
#     
#     #int t_int_price_, int t_size_, int t_order_count_ , int t_level_ , ttime_t t_entry_time_ ,bool t_priority_ = false  
#     def set(self, *argv):
#         self.int_price_ = (int) (argv[0])
#         self.size_ = (int)(argv[1])
#         self.order_count_ = (int)(argv[2])
#         self.level_ = (int)(argv[3])
#         self.order_entry_time_ = (float)(argv[4])
#         if len(argv) == 6 :
#             self.priority_ = (bool)(argv[5])
#   
#     def ToString(self):
#         res = str(self.int_price_) + " " + str(self.size_) + " " + str(self.order_count_)
#         return res

    
class MarketUpdateInfo():
    def __init__(self, *argv):
        self.shortcode_ = ""
        self.security_id_ = 0
#         self.exch_source_ = ""
#         self.storing_pretrade_state_ = False
#         self.pretrade_bestbid_price_  = kInvalidPrice 
#         self.pretrade_bestbid_int_price_ = kInvalidIntPrice 
#         self.pretrade_bestbid_size_ = 0
#         self.pretrade_bestask_price_  = kInvalidIntPrice
#         self.pretrade_bestask_int_price_ = kInvalidIntPrice 
#         self.pretrade_bestask_size_ = 0
#         self.prequote_mkt_size_weighted_price_ = kInvalidPrice  
#         self.last_book_mkt_size_weighted_price_ = kInvalidPrice 
#        self.l1events_ = 0
#        self.trade_update_implied_quote_ = False
        
#         self.bidlevels_ = []
#         self.asklevels_ = []
#         self.bid_level_order_depth_book_ = []
#         self.ask_level_order_depth_book_ = []
        
        if len(argv) == 2:
            self.shortcode_ = argv[0]
            self.security_id_ = (int)(argv[1])
#            self.exch_source_ = argv[2]
        print('MUI.__init__')
        self.bestbid_price_ = kInvalidPrice
        self.bestbid_size_ = 0
        self.bestbid_int_price_ = kInvalidIntPrice
        self.bestbid_ordercount_ = 0
        self.bestask_price_ = kInvalidIntPrice
        self.bestask_size_ = 0
        self.bestask_int_price_ = kInvalidIntPrice
        self.bestask_ordercount_ = 0
        self.spread_increments_ = 1
        self.mkt_size_weighted_price_ = kInvalidPrice
        
#         i=0
#         while i < MAX_LEVELS :
#             self.bidlevels_.append(MarketUpdateInfoLevelStruct ( ))
#             self.asklevels_.append(MarketUpdateInfoLevelStruct ( ))
#             i = i + 1

    
#     def ToString(self):
#         res = "[ " + self.shortcode_
#         if len(self.bidlevels_) >=1 :
#             res += (" " + str(self.bidlevels_ [ 0 ].limit_ordercount_) + str(self.bidlevels_ [ 0 ].limit_size_) + str(self.bidlevels_ [ 0 ].limit_price_) +str(self.bidlevels_ [ 0 ].limit_price_) +str(self.bidlevels_ [ 0 ].limit_size_) +str(self.bidlevels_ [ 0 ].limit_ordercount_))
#         else : 
#             res += " 0 0 0 0 0 0"
#         res +=" ]  [ " + self.bestbid_ordercount_ + " " + self.bestbid_size_ + " " + self.bestbid_price_ + " " + self.bestask_price_ + " " + self.bestask_size_ + " " + self.bestask_ordercount_ + " ]"
#         return res
    
