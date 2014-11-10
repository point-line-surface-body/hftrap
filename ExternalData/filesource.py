from struct import calcsize
from ExternalData.message import Message
from ExternalData.external_data_listener import ExternalDataListener
from struct import unpack
from TradingPlatform.get_data_file_name import GetFileSourceName

class FileSource(ExternalDataListener):
    
    def __init__(self, _watch_, _shortcode_, _smv_, _trading_date_):
        self.watch_ = _watch_
        self.shortcode_ = _shortcode_
        self.smv_ = _smv_
        self.file_name_ = GetFileSourceName(_shortcode_, _trading_date_)
        self.file_ = open(self.file_name_, 'rb')
        bytes_ = self.file_.read(calcsize('Q'))
        self.reference_sec_ = unpack('Q', bytes_)[0]
        
    def __del__(self):
        return
        
    def ProcessThisEvent(self):
        self.watch_.OnTimeReceived(self.next_event_.sec_, self.next_event_.usec_)
        #print  self.shortcode_, self.next_event_.sec_, self.next_event_.usec_
        if (self.next_event_.type_ == 'T'):
            self.smv_.OnTradePrint(self.next_event_.trade_price_, self.next_event_.trade_size_, self.next_event_.buysell_, 
                              self.next_event_.bid_price_, self.next_event_.bid_size_, self.next_event_.bid_orders_, 
                              self.next_event_.ask_price_, self.next_event_.ask_size_, self.next_event_.ask_orders_)
        else:
            self.smv_.OnMarketUpdate(self.next_event_.bid_price_, self.next_event_.bid_size_, self.next_event_.bid_orders_, 
                                     self.next_event_.ask_price_, self.next_event_.ask_size_, self.next_event_.ask_orders_)
    
    def SeekToFirstEventAfter(self, _start_time_):
        print('Filesource.SeekToFirstEventAfter')
        iter_ = 0
        while (1):
            this_bytes_ = self.file_.read(calcsize('QIccHHHHHH'))
            if (len(this_bytes_) < calcsize('QIccHHHHHH')):
                print('False'+' '+str(len(this_bytes_)))
                return False
            self.next_event_ = Message(this_bytes_)
            self.next_event_.sec_ += self.reference_usec_
            self.next_event_timestamp_ = self.next_event_.timestamp_
            if (self.next_event_timestamp_ > _start_time_):
                print('Turned True after '+str(iter_)+' iterations: '+str(self.next_event_timestamp_)+' '+str(_start_time_))
                return True
            iter_ += 1
        print('Never returned true')
        return
    
    def ComputeEarliestDataTimestamp(self):
        this_bytes_ = self.file_.read(calcsize('QIccHHHHHH'))
        if (len(this_bytes_) < calcsize('QIccHHHHHH')):
            self.next_event_timestamp_ = 0
            return False
        else:
            self.next_event_ = Message(this_bytes_)
            self.next_event_.sec_ += self.reference_sec_
            self.next_event_timestamp_ = self.next_event_.timestamp_
            return True
    
    def SetNextTimeStamp(self):
        this_bytes_ = self.file_.read(calcsize('QIccHHHHHH'))
        if (len(this_bytes_) < calcsize('QIccHHHHHH')):
            self.next_event_timestamp_ = 0
            return False
        else:
            self.next_event_ = Message(this_bytes_)
            self.next_event_timestamp_ = self.next_event_.timestamp_
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