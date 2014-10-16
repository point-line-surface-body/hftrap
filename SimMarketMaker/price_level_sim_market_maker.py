from MarketAdapter.security_market_view_change_listener import SecurityMarketViewChangeListener
from ExternalData.external_time_listener import TimePeriodListener

class PriceLevelSimMarketMaker(SecurityMarketViewChangeListener,TimePeriodListener):
    shcToSMMmap = dict()
    def __init__(self, watch_, smv):
        self.watch_ = watch_
        self.dep_market_view_ = smv
        self.bestbid_int_price_ = 0
        self.bestask_int_price_ = 0 
        self.bestbid_size_ = 0
        self.bestask_size_ = 0
        self.dep_market_view_.subscribe_price_type(self, "MktSizeWPrice")
        self.watch_.subscribe_BigTimePeriod(self) # may make small Time period also in watch
        
    @staticmethod
    def GetUniqueInstance(watch_, smv):
        short_code = smv.shortcode()
        if short_code not in PriceLevelSimMarketMaker.shcToSMMmap.keys():
            PriceLevelSimMarketMaker.shcToSMMmap[short_code] = PriceLevelSimMarketMaker(watch_, smv)
        return PriceLevelSimMarketMaker.shcToSMMmap[short_code]
    
    def OnMarketUpdate(self, _security_id_, _market_update_info_):
        return
    
    def OnTradePrint(self, _security_id_, _trade_print_info_, _market_update_info_):
        return
    
    def OnTimePeriodUpdate(self, num_pages_to_add_):
        return