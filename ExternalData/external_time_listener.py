from abc import ABCMeta
from abc import abstractmethod

class ExternalTimeListener():
    __metaclass__ = ABCMeta
    @abstractmethod
    def OnTimeReceived(self, _time_):
        return

class TimePeriodListener():
    __metaclass__ = ABCMeta
    @abstractmethod
    def OnTimePeriodUpdate (self, _num_pages_to_add_):
        return