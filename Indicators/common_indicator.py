from MarketAdapter.security_market_view_change_listener import SecurityMarketViewChangeListener
from CommonTradeUtils.watch import Watch
import core_shortcodes
from indicator_listener import IndicatorListenerPair, UnweightedIndicatorListenerPair
#from CommonTradeUtils.market_update_manager import MarketUpdateManager

class CommonIndicator(SecurityMarketViewChangeListener):
    concise_indicator_description_map_ = dict()
    def __init__(self, *args):
        self.watch = Watch()
        self.concise_indicator_description_ = ""
        self.indicator_listener_pairs_ = []
        self.unweighted_indicator_listener_pairs_ = []
        self.indicator_value_ = 0.0
        self.is_ready = False
        self.data_interupted = False
        self.base_price_type = "MidPrice"
        if len(args) == 3:
            self.__init2__(self, args[0], args[1], args[2])
        if len(args) == 2:
            self.__init2__(self, args[0], args[1])
           
    def __init2__(self, watch,concise_indicator_description_, base_price_type ):
        self.watch = watch
        self.concise_indicator_description_ = concise_indicator_description_
        self.price_type = base_price_type
        
    def __init3__(self, watch,concise_indicator_description_):
        self.watch = watch
        self.concise_indicator_description_ = concise_indicator_description_
        
    def SetBasepxPxtype (self, smv, base_px_type):
        self.base_price_type = base_px_type
 
    def OnGlobalPositionChange ( self, security_id, new_global_pos):
        return
    
    def ConciseIndicatorDescription (self ):
        return  self.concise_indicator_description_
    
    def IsIndicatorReady(self):
        return self.is_ready
    
    def IsDataInterrupted(self):
        return self.data_interupted
    
    def IndicatorValue (self, is_ready):
        if is_ready :
            return self.indicator_value_
        else :
            return 0.0
    
    def WhyNotReady(self):
        return
    
    def GetReadinessRequired(self, r_dep_shortcode_, tokens_):
        core_shortcode_vec_= []
        core_shortcodes.GetCoreShortcodes(r_dep_shortcode_, core_shortcode_vec_)
        if tokens_[3] in core_shortcode_vec_:
            return True
        else:
            return False
    
    def SubscribeDataInterrupts(self,market_update_manager_ ):
        return
    
    def OnIndicatorUpdate ( self, indicator_index_ ,  _new_values_):
        return
 
    def AddIndicatorListener(self, _indicator_index_, _indicator_listener_,  _node_value_):   
        if _indicator_listener_ is not None and not self.IsWeightedListenerPresent(self, _indicator_listener_):
            _new_indicator_listener_pair_ = IndicatorListenerPair(_indicator_index_, _indicator_listener_, _node_value_)
            self.indicator_listener_pairs_.append(_new_indicator_listener_pair_)
    
    def UpdateIndicatorListenerWeight(self, _indicator_listener__, _node_value_):
        for x in range(len(self.indicator_listener_pairs_)):
            if self.indicator_listener_pairs_[x].indicator_listener == _indicator_listener__ :
                self.indicator_listener_pairs_[x].node_value_ = _node_value_ ;
    
    def MultiplyIndicatorListenerWeight (self, _indicator_listener__,_node_value_mult_factor_ ):
        for x in range(len(self.indicator_listener_pairs_)):
            if self.indicator_listener_pairs_[x].indicator_listener == _indicator_listener__ :
                self.indicator_listener_pairs_[x].node_value_ *= _node_value_mult_factor_ ;
  
    def GetIndicatorListenerWeight (self, _indicator_listener__):
        for x in range(len(self.indicator_listener_pairs_)):
            if self.indicator_listener_pairs_[x].indicator_listener == _indicator_listener__ :
                return self.indicator_listener_pairs_[x].node_value_
        return -100000000
    
    def IsWeightedListenerPresent (self,_indicator_listener__ ):
        for x in range(len(self.indicator_listener_pairs_)):
            if self.indicator_listener_pairs_[x].indicator_listener == _indicator_listener__ :
                return True
        return False
    
    def AddUnweightedIndicatorListener(self,_indicator_index_, _indicator_listener__ ):
        if _indicator_listener__ is not None and self.IsUnweightedListenerPresent ( _indicator_listener__ ) == False :
            _new_unweighted_indicator_listener_pair_ = UnweightedIndicatorListenerPair( _indicator_index_, _indicator_listener__ )
            self.unweighted_indicator_listener_pairs_.append(_new_unweighted_indicator_listener_pair_) 
          
    def IsUnweightedListenerPresent(self, _indicator_listener__):
        for x in range(len(self.unweighted_indicator_listener_pairs_)):
            if self.unweighted_indicator_listener_pairs_[x].indicator_listener == _indicator_listener__ :
                return True
        return False
    
    def NotifyIndicatorListeners(self, _indicator_value_):
        for x in range(len(self.indicator_listener_pairs_)):
            self.indicator_listener_pairs_[x].OnIndicatorUpdate ( _indicator_value_ ) 
        for x in range(len(self.unweighted_indicator_listener_pairs_)):
            self.unweighted_indicator_listener_pairs_[x].OnIndicatorUpdate ( _indicator_value_ )