from MarketAdapter.security_market_view import SecurityMarketView

class ShortcodeSecurityMarketViewMap():
    shortcode_smv_map_ = dict()
    unique_instance = dict()
    watch_ = None  
    
    def __init__(self):
        return
    
    @staticmethod
    def GetUniqueInstance(watch):
        if ShortcodeSecurityMarketViewMap.unique_instance.has_key("instance"):
            return ShortcodeSecurityMarketViewMap.unique_instance["instance"]
        else :
            ShortcodeSecurityMarketViewMap.unique_instance["instance"] = ShortcodeSecurityMarketViewMap()
            return ShortcodeSecurityMarketViewMap.unique_instance["instance"]
   
    @staticmethod
    def GetSecurityMarketView ( _shortcode_ ):
        if _shortcode_ in ShortcodeSecurityMarketViewMap.shortcode_smv_map_.keys() :
            return ShortcodeSecurityMarketViewMap.shortcode_smv_map_[_shortcode_]
        else :
            ShortcodeSecurityMarketViewMap.shortcode_smv_map_[_shortcode_] = SecurityMarketView(ShortcodeSecurityMarketViewMap.watch_, _shortcode_, len(ShortcodeSecurityMarketViewMap.shortcode_smv_map_.keys()))
            return ShortcodeSecurityMarketViewMap.shortcode_smv_map_[_shortcode_]
        
    def CheckValid(self, _shortcode_):
        if _shortcode_ in ShortcodeSecurityMarketViewMap.shortcode_smv_map_.keys() :
            return
        else :
            exit()
            return None        
    
    def GetSecurityMarketViewVec(self, _shortcode_vec_,_smvvec_):
        _smvvec_.clear()
        for i in range(len(_shortcode_vec_)):
            _smvvec_.append(self.GetSecurityMarketView ( _shortcode_vec_ [ i ] ) )
            
    #  _security_market_view__ should be reference
    def AddEntry(self,_shortcode_, _security_market_view__ ):
        if _security_market_view__ is not None :
            ShortcodeSecurityMarketViewMap.shortcode_smv_map_[_shortcode_] = _security_market_view__
            
    @staticmethod
    def StaticCheckValid(_shortcode_):
        return ShortcodeSecurityMarketViewMap.GetUniqueInstance().CheckValid ( _shortcode_ )
    
    def StaticGetSecurityMarketView(self,_shortcode_ ) :
        return ShortcodeSecurityMarketViewMap.GetUniqueInstance().GetSecurityMarketView ( _shortcode_ )

        
        