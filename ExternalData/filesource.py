from struct import calcsize
from ExternalData.message import Message
from ExternalData.external_data_listener import ExternalDataListener
from TradingPlatform.get_data_file_name import GetFileSourceName

class FileSource(ExternalDataListener):
    
    def __init__(self, _watch_, _shortcode_, _smv_, _trading_date_):
        self.watch_ = _watch_
        self.shortcode_ = _shortcode_
        self.smv_ = _smv_
        self.file_name_ = GetFileSourceName(_shortcode_, _trading_date_)
        self.file_ = open(self.file_name_, 'rb')
        
    def __del__(self):
        return
        
    def ProcessThisEvent(self):
        self.watch_.OnTimeReceived(self.next_event.timestamp)
        '''OnTradePrint'''
        if (self.next_event_.type == 'T'):
            '''TODO: Fill this'''
            self.smv_.OnTrade()
        else:
            '''TODO: fill this'''
            self.smv_.OnL1PriceUpdate()
    
    def SeekToFirstEventAfter(self, _start_time_):
        while (1):
            this_bytes_ = self.file_.read(calcsize('fcHHHHHH'))
            if (len(this_bytes_) < calcsize('fcHHHHHH')):
                return False
            self.next_event_ = Message(this_bytes_)
            self.next_event_timestamp_ = self.next_event_.timestamp_
            if (self.next_event_timestamp_ > _start_time_):
                return True
        return
    
    def ComputeEarliestDataTimestamp(self):
        this_bytes_ = self.file_.read(calcsize('fcHHHHHH'))
        if (len(this_bytes_) < calcsize('fcHHHHHH')):
            self.next_event_timestamp_ = 0
            return False
        else:
            self.next_event_ = Message(this_bytes_)
            self.next_event_timestamp_ = self.next_event_.timestamp_
            return True
    
    def SetNextTimeStamp(self):
        '''@Ashwin Can it be less than zero?'''
        if (self.events_left_ <= 0):
            self.events_left_ = 0
            '''Why Non Intermediate?'''
            found_non_intermediate_event_ = False
            while (not found_non_intermediate_event_):
                if (self.file_.read(self.next_event, )): #TODO
                    self.next_event_timestamp_ = 0
                    return False
                if (self.next_event_.time_ != 0):
                    next_non_intermediate_time_ = self.next_event_.time_
                    found_non_intermediate_event_ = True
            self.event_queue_.append(self.next_event_)
            self.events_left_ += 1
        if (self.events_left_ > 0):
            self.next_event_ = self.event_queue_[0]
            self.next_event_timestamp_ = next_non_intermediate_time_
            self.events_left_ -= 1
            self.event_queue_.pop()
            return True
        return True
        
    def ProcessAllEvents(self):
        while (1):
            self.ProcessThisEvent()
            if (not self.SetNextTimeStamp()):
                return
            
    def ProcessEventsTill(self, _end_time_):
        while (self.next_event_timestamp_ <= _end_time_):
            self.ProcessThisEvent()
            if (not self.SetNextTimeStamp()):
                return