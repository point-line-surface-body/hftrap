from MarketAdapter.security_market_view_change_listener import SecurityMarketViewChangeListener
from ExternalData.external_time_listener import TimePeriodListener
from OrderManager.base_sim_market_maker import BaseSimMarketMaker

class PriceLevelSimMarketMaker(BaseSimMarketMaker, SecurityMarketViewChangeListener,TimePeriodListener):
    shcToSMMmap = dict()
    def __init__(self, watch_, smv):
        self.watch_ = watch_
        self.dep_market_view_ = smv
        self.bestbid_int_price_ = 0
        self.bestask_int_price_ = 0 
        self.bestbid_size_ = 0
        self.bestask_size_ = 0
        self.last_bid_size_change_msecs_ = 0
        self.last_ask_size_change_msecs_ = 0
        self.ask_side_priority_order_exists_ = False
        self.ask_side_priority_order_size_ = 0
        self.bid_side_priority_order_exists_ = False
        self.bid_side_priority_order_size_ = 0
        self.dep_market_view_.subscribe_price_type(self, "MktSizeWPrice")
        self.watch_.subscribe_BigTimePeriod(self) # may make small Time period also in watch
        
    @staticmethod
    def GetUniqueInstance(watch_, smv):
        short_code = smv.shortcode()
        if short_code not in PriceLevelSimMarketMaker.shcToSMMmap.keys():
            PriceLevelSimMarketMaker.shcToSMMmap[short_code] = PriceLevelSimMarketMaker(watch_, smv)
        return PriceLevelSimMarketMaker.shcToSMMmap[short_code]
    
    def OnMarketUpdate(self, _security_id_, _market_update_info_):
        old_bestbid_int_price_ = self.bestbid_int_price_
        old_bestbid_size_ = self.bestbid_size_
        old_bestask_int_price_ = self.bestask_int_price_
        old_bestask_size_ = self.bestask_size_
        if self.bestbid_size_ < _market_update_info_.bestbid_size_ :
            self.last_bid_size_change_msecs_ = self.watch_.GetMsecsFromMidnight()
        if self.bestask_size_ < _market_update_info_.bestask_size_  :
            self.last_ask_size_change_msecs_ = self.watch_.GetMsecsFromMidnight()
        if old_bestask_int_price_ > _market_update_info_.bestask_int_price_ :
            if self.dep_market_view_.market_update_info_.asklevels_[0].limit_ordercount_ ==1:
                self.ask_side_priority_order_exists_ = True
                self.ask_side_priority_order_size_ = self.dep_market_view_.market_update_info_.asklevels_[0].limit_size_
            else:
                self.ask_side_priority_order_exists_ = False
                self.ask_side_priority_order_size_ = 0
        if old_bestbid_int_price_ < _market_update_info_.bestbid_int_price_ :
            if self.dep_market_view_.market_update_info_.bidlevels_[0].limit_ordercount_ ==1 :
                self.bid_side_priority_order_exists_ = True
                self.bid_side_priority_order_size_ = self.dep_market_view_.market_update_info_.bidlevels_[0].limit_size_
            else :
                self.bid_side_priority_order_exists_ = False
                self.bid_side_priority_order_size_ = 0
        
        







        
    
    def OnTradePrint(self, _security_id_, _trade_print_info_, _market_update_info_):
        return
    
    def OnTimePeriodUpdate(self, num_pages_to_add_):
        return