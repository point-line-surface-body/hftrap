class StrategyLine():
    def __init__(self):
        self.runtime_id_ = 0
        self.trading_start_ttime_t_ = 0
        self.trading_end_ttime_t_ = 0
        self.trading_start_utc_mfm_ = 8*60*60*1000
        self.trading_end_utc_mfm_ = 8*60*60*1000
        self.p_dep_market_view_ = None
        self.p_base_trader_ = None
        #self.exec_ = None
        self.strategy_full_line_ = ""
        self.dep_shortcode_ = "invalid"
        self.strategy_name_ = "invalid"
        self.model_filename_ = "invalid"
        self.param_filename_ = "invalid"
        #self.trading_manager_ = None
        #self.pair_exec_ = None

class StrategyDesc():
    
    def __init__(self, _strategy_desc_filename_, tradingdate_):
        self.strategy_desc_filename_ = _strategy_desc_filename_
        self.strategy_vec_ = []
        #self.simconfig_filename_ = ""
        strategy_desc_file_ = open(self.strategy_desc_filename_)
        for line_ in strategy_desc_file_:
            tokens_ = line_.split()
            if len(tokens_) >= 7 and tokens_[0] == "STRATEGYLINE": # tokens[8] = traded zone, so skipping it
                t_new_strategy_line_ = StrategyLine()
                t_new_strategy_line_.dep_shortcode_ = tokens_[1]
                t_new_strategy_line_.strategy_name_ = tokens_[2]
                t_new_strategy_line_.model_filename_ = tokens_[3]
                t_new_strategy_line_.paramfilename_ = tokens_[4]
                t_new_strategy_line_.trading_start_ttime_t_ = tokens_[5]
                t_new_strategy_line_.trading_start_utc_mfm_ = 0 #GetMsecsFromMidnightFromHHMMSS(tokens_[5])
                t_new_strategy_line_.trading_end_ttime_t_ = tokens_[6]
                t_new_strategy_line_.trading_end_utc_mfm_= 0 #GetMsecsFromMidnightFromHHMMSS(tokens_[6])
                t_new_strategy_line_.runtime_id_ = (int)(tokens_[7])
                #if len(tokens_):
                #    self.simconfig_filename_ = tokens_[7]
                t_new_strategy_line_.strategy_full_line_ = line_
                for i in range(len(self.strategy_vec_)):
                    if self.trategy_vec_[i].runtime_id_ == t_new_strategy_line_.runtime_id_:
                        exit()
                self.strategy_vec_.append(t_new_strategy_line_)
        
    def GetMinStartTime(self):
        retval_ = self.strategy_vec_[0].trading_start_ttime_t_
        i = 1
        while i < len(self.strategy_vec_) :
            if self.strategy_vec_[i].trading_start_ttime_t_ < retval_ : 
                retval_ = self.strategy_vec_[i].trading_start_ttime_t_
            i+=1
        return retval_
    
    def GetMaxEndTime(self):
        retval_ = self.strategy_vec_[0].trading_end_ttime_t
        i = 1
        while i < len(self.strategy_vec_) :
            if self.strategy_vec_[i].trading_end_ttime_t_ > retval_ : 
                retval_ = self.strategy_vec_[i].trading_end_ttime_t_
            i+=1
        return retval_
    
    def AllDependantsSame(self):
        if len(self.strategy_vec_) < 2:
            return True
        else :
            i=2
            while i < len(self.strategy_vec_) : 
                if self.strategy_vec_[i].dep_shortcode_ != self.strategy_vec_[0].dep_shortcode_ :
                    return False
                i += 1
        return True
    
    #Dont need this function ??
    #@staticmethod
    #def GetRollParam(_paramfile_,_tradingdate_ ):
    #    return _paramfile_