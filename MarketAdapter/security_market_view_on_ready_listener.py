from abc import ABCMeta
from abc import abstractmethod


class SecurityMarketViewOnReadyListener:
    __metaclass__ = ABCMeta
    @abstractmethod
    def SMVOnReady(self):
        return
        
        
        