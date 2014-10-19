from struct import calcsize
from ExternalData.message import Message
from ExternalData.external_data_listener import ExternalDataListener
from TradingPlatform.get_data_file_name import GetFileSourceName
from MarketAdapter.basic_market_view import MarketUpdateInfo, TradePrintInfo

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
        self.watch_.OnTimeReceived(self.next_event_.sec_, self.next_event_.usec_)
        '''OnTradePrint'''
        if (self.next_event_.type_ == 'T'):
            '''TODO: Fill this'''
            trade_print_info_ = TradePrintInfo()
            trade_print_info_.buysell_ = self.next_event_.buysell_
            trade_print_info_.int_trade_price_ = self.next_event_.trade_price_
            trade_print_info_.size_traded_ = self.next_event_.trade_size_
        else:
            '''TODO: fill this'''
            smv_.OnMarketUpdate()
            
            
            market_update_info_ = MarketUpdateInfo()
            market_update_info_.bestbid_int_price_ = self.next_event_.bid_price_
            market_update_info_.bestbid_ordercount_ = self.next_event_.bid_orders_
            market_update_info_.bestbid_size_ = self.next_event_.bid_size_
            market_update_info_.bestask_int_price_ = self.next_event_.ask_price_
            market_update_info_.bestask_ordercount_ = self.next_event_.ask_size_
            market_update_info_.bestask_size_ = self.next_event_.ask_size_
    
    def SeekToFirstEventAfter(self, _start_time_):
        print('Filesource.SeekToFirstEventAfter')
        iter_ = 0
        while (1):
            this_bytes_ = self.file_.read(calcsize('QIccHHHHHHHH'))
            if (len(this_bytes_) < calcsize('QIccHHHHHHHH')):
                print('False'+' '+str(len(this_bytes_)))
                return False
            self.next_event_ = Message(this_bytes_)
            self.next_event_timestamp_ = self.next_event_.timestamp_
            if (self.next_event_timestamp_ > _start_time_):
                print('Turned True after '+str(iter_)+' iterations: '+str(self.next_event_timestamp_)+' '+str(_start_time_))
                return True
            iter_ += 1
        print('Never returned true')
        return
    
    def ComputeEarliestDataTimestamp(self):
        this_bytes_ = self.file_.read(calcsize('QIccHHHHHHHH'))
        if (len(this_bytes_) < calcsize('QIccHHHHHHHH')):
            self.next_event_timestamp_ = 0
            return False
        else:
            self.next_event_ = Message(this_bytes_)
            self.next_event_timestamp_ = self.next_event_.timestamp_
            return True
    
    def SetNextTimeStamp(self):
        this_bytes_ = self.file_.read(calcsize('QIccHHHHHHHH'))
        if (len(this_bytes_) < calcsize('QIccHHHHHHHH')):
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