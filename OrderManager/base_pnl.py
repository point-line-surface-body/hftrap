from MarketAdapter.security_market_view_change_listener import SecurityMarketViewChangeListener
from OrderManager.order_manager_listeners import ExecutionListener

class BasePnl(ExecutionListener, SecurityMarketViewChangeListener):
    
    def __init__(self, _watch_, _order_manager_, _dep_market_view_, _runtime_id_):
        self.watch_ = _watch_
        self.order_manager_ = _order_manager_
        self.dep_market_view_ = _dep_market_view_
        self.runtime_id_ = _runtime_id_
        self.pnl_ = 0
        self.realized_pnl_ = 0
        self.position_ = 0
        
    def OnMarketUpdate(self, _security_id_, _market_update_info_):
        return
    
    def OnTradePrint(self, _security_id_, _trade_print_info_, _market_update_info_):
        return
        
    def OnExec(self, _new_position_, _exec_quantity_, _buysell_, _price_, _int_price_):
        return
    
    def LogTrade(self):
        return