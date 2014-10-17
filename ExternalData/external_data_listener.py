from abc import ABCMeta
from abc import abstractmethod

class ExternalDataListener():
    __metaclass__ = ABCMeta
    def __init__(self):
        self.next_event_timestamp = 0
        return
    
    def __del__(self):
        return
    
    def __lt__(self, other):
        return self.NextEventTimestamp() < other.NextEventTimestamp()
    
    def socket_file_descriptor(self):
        return
    
    @abstractmethod
    def SeekToFirstEventAfter(self, time, has_events):
        return
    
    @abstractmethod
    def ComputeEarliestDataTimestamp(self, has_events):
        return
    
    @abstractmethod
    def ProcessAllEvents(self):
        return
    
    @abstractmethod
    def ProcessEventsTill(self, _end_time_):
        return
        
    def NextEventTimestamp(self):
        return self.next_event_timestamp