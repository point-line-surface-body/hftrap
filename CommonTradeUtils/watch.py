from time import gmtime
from ExternalData.external_time_listener import ExternalTimeListener

class Watch(ExternalTimeListener):
    
    def __init__(self, _trading_date_):
        self.trading_date_ = _trading_date_
        self.tv_sec_ = 0
        self.tv_usec_ = 0
        self.msecs_from_midnight_ = 0
        self.prev_midnight_sec_ = 0
        
    def OnTimeReceived(self, _tv_sec_, _tv_usec_):
        if (self.tv_sec_ == 0):
            t_time = gmtime(_tv_sec_)
            t_date = str(t_time.tm_year)+str(t_time.tm_mon)+str(t_time.tm_day)
            if (not t_date == self.trading_date_):
                print 'Warning: Trading Date not equal to Time Received'
            self.msecs_from_midnight_ = _tv_sec_ % 3600
            self.prev_midnight_sec_ = _tv_sec_ - self.msecs_from_midnight_
            self.tv_sec_ = _tv_sec_
            self.tv_usec_ = _tv_usec_
        else:
            if (_tv_sec_ > self.tv_sec_ or (_tv_sec_ == self.tv_sec_ and _tv_usec_ > self.tv_usec_)):
                self.msecs_from_midnight_ = _tv_sec_ * 1000 + _tv_usec_ / 1000 - self.prev_midnight_sec_
                self.tv_sec_ = _tv_sec_
                self.tv_usec_ = _tv_usec_
        
    def GetMsecsFromMidnight(self):
        return self.msecs_from_midnight_