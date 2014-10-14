from ExternalData.external_time_listener import ExternalTimeListener
import time

class Watch(ExternalTimeListener):
    
    def __init__(self, trading_date):
        self.tv = 0.0
        self.msecs_from_midnight = 0.0
        self.last_midnight_sec_ = 0.0
        self.trading_date = trading_date
        
    def OnTimeReceived(self, new_tv):
        self.tv = new_tv
        t = time.gmtime(new_tv)
        hr = t.tm_hour
        mins = t.tm_min
        secs = t.tm_sec
        secs = hr*60*60 + mins*60 + secs
        msec = (float)(new_tv)*1000 %1000
        self.last_midnight_sec_ = self.msecs_from_midnight
        self.msecs_from_midnight = secs * 1000 + msec
        
        
    def YYMMDD(self):
        return self.trading_date
    
    def tv(self):
        return self.tv