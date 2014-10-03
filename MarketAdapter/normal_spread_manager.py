from CDef.defines import BASESYSINFODIR
import os.path
from os.path import expanduser
import datetime.date
import datetime.timedelta

class NormalSpreadManager():
    t_isodate_to_normal_spread_manager_map_ = dict()
    
    @staticmethod
    def GetUniqueInstance(yymmdd):
        if yymmdd in NormalSpreadManager.t_isodate_to_normal_spread_manager_map_.keys() :
            return NormalSpreadManager.t_isodate_to_normal_spread_manager_map_[yymmdd]
        else :
            NormalSpreadManager.t_isodate_to_normal_spread_manager_map_[yymmdd] = NormalSpreadManager(yymmdd)
            return NormalSpreadManager.t_isodate_to_normal_spread_manager_map_[yymmdd]
            
    def __init__(self, yymmdd):
        self.yymmdd_ = yymmdd
        self.t_normal_spread_info_filename_ = "None"
        self.shortcode_normal_spread_increment_map_ = dict()  
        this_yyyymmdd_ = (int)(yymmdd)
        i=0
        while i < 180 :
            #might need to change the path here
            self.t_normal_spread_info_filename_ = BASESYSINFODIR  + "TradingInfo/NormalSpreadInfo/normal_spread_info_"  + str(this_yyyymmdd_) + ".txt"
            home = expanduser("~")
            self.t_normal_spread_info_filename_ = home + self.t_normal_spread_info_filename_
            if os.path.isfile(self.t_normal_spread_info_filename_):
                break
            else :
                d = datetime.date(this_yyyymmdd_/10000, (this_yyyymmdd_%10000)/100, (this_yyyymmdd_%100))
                d = d - datetime.timedelta(days=1)
                this_yyyymmdd_ = d.year * 10000 + d.month * 100 + d.day
            i += 1
            
        if not os.path.isfile(self.t_normal_spread_info_filename_):
            self.t_normal_spread_info_filename_ = BASESYSINFODIR  + "TradingInfo/NormalSpreadInfo/normal_spread_info_default.txt"
            home = expanduser("~")
            self.t_normal_spread_info_filename_ = home + self.t_normal_spread_info_filename_
        self.LoadNormalSpreadInfoFile ()
             
    @staticmethod
    def GetNormalSpreadIncrements(yymmdd, shortcode):
        return NormalSpreadManager.t_isodate_to_normal_spread_manager_map_[yymmdd].t_GetNormalSpreadIncrements ( shortcode )
    
    def t_GetNormalSpreadIncrements (self, t_shortcode_ ):
        if t_shortcode_ not in self.shortcode_normal_spread_increment_map_.keys() :
            return 1.0
        else :
            return self.shortcode_normal_spread_increment_map_[t_shortcode_]
    
    def LoadNormalSpreadInfoFile(self):
        f = open(self.t_normal_spread_info_filename_)
        line = f.readline()
        while line is not None :
            tokens_ = line.split()
            if len(tokens_) >=2 :               
                self.shortcode_normal_spread_increment_map_[tokens_[0]] = (float)(tokens_[1])
        f.close()
        
        