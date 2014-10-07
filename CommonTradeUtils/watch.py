from ExternalData.external_time_listener import ExternalTimeListener
import os
import commands

class Watch(ExternalTimeListener):
    
    def __init__(self, trading_date):
        self.tv = 0.0
        self.msecs_from_midnight = 0.0
        self.last_midnight_sec_ = 0.0
        self.trading_date = trading_date
        
    def OnTimeReceived(self, new_tv):
        self.tv = new_tv
        command = "date -d @" + str(new_tv)
        res = commands.getoutput(command)
        sec = (float)(res.split(":")[-1].split()[0])
        msec = (float)(new_tv)*1000 %1000
        self.last_midnight_sec_ = self.msecs_from_midnight
        self.msecs_from_midnight = sec * 1000 + msec
        
        
    def YYMMDD(self):
        return self.trading_date
    
    def tv(self):
        return self.tv