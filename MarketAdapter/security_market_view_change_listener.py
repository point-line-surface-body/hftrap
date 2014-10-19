from abc import ABCMeta
from abc import abstractmethod

class SecurityMarketViewChangeListener():
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def OnMarketUpdate(self, _market_update_info_):
        return
    
    @abstractmethod
    def OnTradePrint(self, _trade_print_info_, _market_update_info_):
        return