HIGH_THRESHOLD_VALUE = 100

class TradeVars:
    
    def __init__(self):
        self.l1bid_place_ = HIGH_THRESHOLD_VALUE
        self.l1bid_keep_ = HIGH_THRESHOLD_VALUE
        self.l1bid_improve_ = HIGH_THRESHOLD_VALUE
        self.l1bid_improve_keep_ = HIGH_THRESHOLD_VALUE
        self.l1bid_aggressive = HIGH_THRESHOLD_VALUE
        self.l1bid_trade_size_ = HIGH_THRESHOLD_VALUE
        
        self.l1ask_place_ = HIGH_THRESHOLD_VALUE
        self.l1ask_keep_ = HIGH_THRESHOLD_VALUE
        self.l1ask_improve_ = HIGH_THRESHOLD_VALUE
        self.l1ask_improve_keep_ = HIGH_THRESHOLD_VALUE
        self.l1ask_aggressive_ = HIGH_THRESHOLD_VALUE
        self.l1ask_trade_size_ = HIGH_THRESHOLD_VALUE
        
    def Assign(self, _l1bid_place_, _l1bid_keep_, _l1bid_improve_, _l1bid_improve_keep_, _l1bid_aggressive_, _l1bid_trade_size_, 
                       _l1ask_place_, _l1ask_keep_, _l1ask_improve_, _l1ask_improve_keep_, _l1ask_aggressive_, _l1ask_trade_size_):
        self.l1bid_place_ = _l1bid_place_
        self.l1bid_keep_ = _l1bid_keep_
        self.l1bid_improve_ = _l1bid_improve_
        self.l1bid_improve_keep_ = _l1bid_improve_keep_
        self.l1bid_aggressive = _l1bid_aggressive_
        self.l1bid_trade_size_ = _l1bid_trade_size_
        
        self.l1ask_place_ = _l1ask_place_
        self.l1ask_keep_ = _l1ask_keep_
        self.l1ask_improve_ = _l1ask_improve_
        self.l1ask_improve_keep_ = _l1ask_improve_keep_
        self.l1ask_aggressive_ = _l1ask_aggressive_
        self.l1ask_trade_size_ = _l1ask_trade_size_