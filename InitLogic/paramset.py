class ParamSet:
    
    def __init__(self, _paramfilename_):
        self.LoadParams(_paramfilename_)
    
    '''Currently thresholds are independent of position'''    
    def LoadParams(self, _paramfilename_):
        t_param_file_ = open(_paramfilename_, 'r')
        self.max_int_spread_to_place_ = 5
        while (1):
            t_line_ = t_param_file_.readline()
            if (t_line_ is None or t_line_ == ""):
                break
            t_tokens_ = t_line_.split()
            if (len(t_tokens_) < 3):
                print 'Incorrect Param File'
                return
            assert t_tokens_[0] == 'PARAMVALUE'
            if (t_tokens_[1] == 'WORST_CASE_POSITION'):
                self.worst_case_position_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'UNIT_TRADE_SIZE'):
                self.unit_trade_size_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MAX_POSITION'):
                self.max_position_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'ALLOWED_TO_AGGRESS'):
                self.allowed_to_aggress_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'ALLOWED_TO_IMPROVE'):
                self.allowed_to_improve_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MAX_LOSS'):
                self.max_loss_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MAX_OPENTRADE_LOSS'):
                self.max_opentrade_loss_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MAX_PNL'):
                self.max_pnl_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'SAFE_DISTANCE'):
                self.safe_distance_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'COOLOFF_INTERVAL'):
                self.cooloff_interval_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'AGG_COOLOFF_INTERVAL'):
                self.agg_cooloff_interval_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'BID_KEEP_THRESHOLD'):
                self.bid_keep_threshold_ = float(t_tokens_[2])
            elif (t_tokens_[1] == 'BID_PLACE_THRESHOLD'):
                self.bid_place_threshold_ = float(t_tokens_[2])
            elif (t_tokens_[1] == 'BID_AGGRESS_THRESHOLD'):
                self.bid_aggress_threshold_ = float(t_tokens_[2])
            elif (t_tokens_[1] == 'BID_IMPROVE_KEEP_THRESHOLD'):
                self.bid_improve_keep_threshold_ = float(t_tokens_[2])
            elif (t_tokens_[1] == 'BID_IMPROVE_THRESHOLD'):
                self.bid_improve_threshold_ = float(t_tokens_[2])
            elif (t_tokens_[1] == 'MAX_POSITION_TO_LIFT'):
                self.max_position_to_lift_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MAX_POSITION_TO_CANCEL_ON_LIFT'):
                self.max_position_to_cancel_on_lift_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MAX_INT_SPREAD_TO_CROSS'):
                self.max_int_spread_to_cross_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MAX_POSITION_TO_IMPROVE'):
                self.max_position_to_improve_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MIN_INT_SPREAD_TO_IMPROVE'):
                self.min_int_spread_to_improve_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MIN_POSITION_TO_HIT'):
                self.min_position_to_hit_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MIN_POSITION_TO_CANCEL_ON_HIT'):
                self.min_position_to_cancel_on_hit_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'MIN_POSITION_TO_IMPROVE'):
                self.min_position_to_improve_ = int(t_tokens_[2])
            elif (t_tokens_[1] == 'ASK_KEEP_THRESHOLD'):
                self.ask_keep_threshold_ = float(t_tokens_[2])
            elif (t_tokens_[1] == 'ASK_PLACE_THRESHOLD'):
                self.ask_place_threshold_ = float(t_tokens_[2])
            elif (t_tokens_[1] == 'ASK_AGGRESS_THRESHOLD'):
                self.ask_aggress_threshold_ = float(t_tokens_[2])
            elif (t_tokens_[1] == 'ASK_IMPROVE_KEEP_THRESHOLD'):
                self.ask_improve_keep_threshold_ = float(t_tokens_[2])
            elif (t_tokens_[1] == 'ASK_IMPROVE_THRESHOLD'):
                self.ask_improve_threshold_ = float(t_tokens_[2])
            else:
                print 'Invalid Param'
                exit(0)