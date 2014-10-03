from ExternalData.external_time_listener import ExternalTimeListener

class Watch(ExternalTimeListener):
    
    def __init__(self):
        self.tv = 0.0
        self.msecs_from_midnight = 0.0
        self.last_midnight_sec_ = 0.0
        
    def OnTimeReceived(self, new_tv):
        return
        
    def YYMMDD(self):
        return
    
    def tv(self):
        return