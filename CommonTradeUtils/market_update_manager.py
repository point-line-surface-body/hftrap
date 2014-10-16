from MarketAdapter.security_market_view_change_listener import SecurityMarketViewChangeListener
from ExternalData.external_time_listener import TimePeriodListener

MIN_MSEC_DURATION = 5000

class MarketUpdateManager(TimePeriodListener, SecurityMarketViewChangeListener):
    unique_instance = None
    
    def __init__(self,_watch_,_sid_to_smv_ptr_map_,_trading_date_):
        self.watch_ = _watch_
        self.security_id_to_smv_ = _sid_to_smv_ptr_map_ # its an array
        self.trading_date_ = _trading_date_
        self.check_updates_ = False
        self.security_id_to_smv_ = []
        self.last_check_msecs_from_midnight_ = 0
        min_msec_market_update_ = 60000 # we can change this, or we can put different for different security
        '''might not need following variables'''
        security_id_to_last_msec_market_update_ = [0 for i in range(len(_sid_to_smv_ptr_map_))]
    
    @staticmethod
    def GetUniqueInstance(_watch_,_sid_to_smv_ptr_map_,_trading_date_):
        if MarketUpdateManager.unique_instance == None :
            MarketUpdateManager.unique_instance = MarketUpdateManager(_watch_,_sid_to_smv_ptr_map_,_trading_date_)
        return MarketUpdateManager.unique_instance
    
    def OnMarketUpdate(self,_security_id_, _market_update_info_):
        if not self.check_updates_ :
            return 
        if _security_id_ >= len(self.security_id_to_smv_) :
            return
        if self.security_id_to_smv_[_security_id_] is None :
            return
        self.security_id_to_last_msec_market_update_[_security_id_] = self.watch_.GetMsecsFromMidnight()
          
    def OnTradePrint(self,_security_id_,_trade_print_info_,_market_update_info_):
        self.OnMarketUpdate(_security_id_,_market_update_info_)
        
    def StartListening(self):
        for smv in self.security_id_to_smv_ :
            smv.subscribe_L1_Only(self)
        '''not sure if we need this '''
        self. watch_.subscribe_BigTimePeriod (self)
    
    def start(self):
        self.StartListening()
        self.check_updates_ = True
        
    def stop(self):
        self.check_updates_ = False
    
    '''overriding function of TimePeriodListener'''
    def OnTimePeriodUpdate (self, num_pages_to_add_):
        if not self.check_updates_ :
            return
        msecs_from_midnight_ = self.watch_.GetMsecsFromMidnight()
        if msecs_from_midnight_ > self.last_check_msecs_from_midnight_ + MIN_MSEC_DURATION :
            self.last_check_msecs_from_midnight_ = msecs_from_midnight_
            

