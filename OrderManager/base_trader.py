# BaseSimTrader must extend this
class BaseTrader:
    
    def SendTrade(self, _order_, _is_fok_):
        return
    
    def CancelTrade(self, _order_):
        return
    
    def ModifyTrade(self, _order_, _new_size_requested_):
        return
    
    def ReplayTrade(self, _order_):
        return
    
    # May not be used
    def GetClientId(self):
        return