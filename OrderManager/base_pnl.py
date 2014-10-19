from MarketAdapter.security_market_view_change_listener import SecurityMarketViewChangeListener
from OrderManager.order_manager_listeners import ExecutionListener
from CDef.security_definitions import SecurityDefinitions
class BasePnl(ExecutionListener, SecurityMarketViewChangeListener):
    
    def __init__(self, _watch_, _order_manager_, _dep_market_view_, _runtime_id_):
        self.watch_ = _watch_
        self.order_manager_ = _order_manager_
        self.dep_market_view_ = _dep_market_view_
        self.runtime_id_ = _runtime_id_
        self.pnl_ = 0
        self.realized_pnl_ = 0
        self.position_ = 0
        self.current_price_ = 0
        self.last_bid_price_ = 0
        self.last_ask_price_ = 0
        self.total_pnl_ = 0
        self.numbers_to_dollars_ = 1
        self.min_pnl_till_now_ = 0
        self.opentrade_unrealized_pnl_ = 0
        self.realized_pnl_ = 0
        
        
    def OnMarketUpdate(self, _security_id_, _market_update_info_):
        self.current_price_ = _market_update_info_.mkt_size_weighted_price_
        self.last_bid_price_ =  _market_update_info_.bestbid_price_
        self.last_ask_price_ = _market_update_info_.bestask_price_
        self.numbers_to_dollars_ = SecurityDefinitions.contract_specification_map_[_market_update_info_.shortcode_].num_to_dollars_
        self.total_pnl_ = self.pnl_ + (self.position_ * self.current_price_ * self.numbers_to_dollars_)
        if self.total_pnl_ < self.min_pnl_till_now_ :
            self.min_pnl_till_now_ = self.total_pnl_
        self.opentrade_unrealized_pnl_ = self.total_pnl_ - self.realized_pnl_
        
    
    def OnTradePrint(self, _security_id_, _trade_print_info_, _market_update_info_):
        return
        
    def OnExec(self, _new_position_, _exec_quantity_, _buysell_, _price_, _int_price_):
        return
    
    def LogTrade(self):
        return