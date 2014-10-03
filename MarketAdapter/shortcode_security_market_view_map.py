class ShortcodeSecurityMarketViewMap():
    shortcode_smv_map_ = dict()
   
    #make this function
    @staticmethod
    def GetUniqueInstance():
        return 
   
    def GetSecurityMarketView ( self,  _shortcode_ ):
        if _shortcode_ in ShortcodeSecurityMarketViewMap.shortcode_smv_map_.keys() :
            return ShortcodeSecurityMarketViewMap.shortcode_smv_map_[_shortcode_]
        else :
            return None
        
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

        
        