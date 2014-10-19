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
        self.commish_dollars_per_unit_ = 0
        
        
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
        
    def OnExec(self, new_position_, _exec_quantity_, _buysell_, _price_, _int_price_):
        abs_change_position_ = abs(new_position_ - self.position_)
        self.current_price_ = _price_
        if _buysell_ == "BUY" :
            if self.position_ < 0 and new_position_ >=0 :
                # position and new_position are of different sign, So need to break trades into 2 parts.. Firstlt closing the position
                trade1size = -1 * self.position_
                self.pnl_ -= trade1size * _price_ * self.numbers_to_dollars_
                self.pnl_ -= trade1size * self.commish_dollars_per_unit_
                self.last_closing_trade_pnl_ = self.pnl_ - self.realized_pnl_
                self.realized_pnl_ = self.pnl_
                #remaining part of trade
                trade2size = new_position_
                if trade2size == 0 :
                    self.total_pnl_= self.pnl_
                    if self.total_pnl_ < self.min_pnl_till_now_ :
                        self.min_pnl_till_now_ = self.total_pnl_
                    self.average_open_price_ = 0.0 #flat
                else :
                    self.pnl_ -= trade2size * _price_ * self.numbers_to_dollars_
                    self.pnl_ -= trade2size * self.commish_dollars_per_unit_
                    self.average_open_price_ = _price_ # open part is entirely upto this price
                    self.total_pnl_ = self.pnl_ + new_position_ * self.current_price_ * self.numbers_to_dollars_
                    if self.total_pnl_ < self.min_pnl_till_now_ :
                        self.min_pnl_till_now_ = self.total_pnl_
                    self.opentrade_unrealized_pnl_ = self.total_pnl_ - self.realized_pnl_
            else :
                self.pnl_ -= abs_change_position_ * _price_ * self.numbers_to_dollars_
                self.pnl_ -= abs_change_position_ * self.commish_dollars_per_unit_
                self.total_pnl_ = self.pnl_ + new_position_ * self.current_price_ * self.numbers_to_dollars_
                if self.total_pnl_ < self.min_pnl_till_now_ :
                    self.min_pnl_till_now_ = self.total_pnl_
                self.opentrade_unrealized_pnl_ = self.total_pnl_ - self.realized_pnl_
                self.average_open_price_ = (self.average_open_price_ * self.position_ + _price_* (new_position_ - self.position_))/new_position_
        else :
            if self.position_ > 0 and new_position_ <=0 :
                trade1size = self.position_
                self.pnl_ += trade1size * _price_ * self.numbers_to_dollars_
                self.pnl_ -= trade1size * self.commish_dollars_per_unit_
                self.last_closing_trade_pnl_ = self.pnl_ - self.realized_pnl_
                self.realized_pnl_ = self.pnl_
                
                trade2size = ( abs_change_position_ - trade1size )
                if trade2size ==0 :
                    self.total_pnl_ = self.pnl_
                    if self.total_pnl_ < self.min_pnl_till_now_ :
                        self.min_pnl_till_now_ = self.total_pnl_
                    self.average_open_price_ = 0.0
                else :
                    self.pnl_ += trade2size * _price_ * self.numbers_to_dollars_
                    self.pnl_ -= trade2size * self.commish_dollars_per_unit_
                    self.average_open_price_ = _price_
                    self.total_pnl_ = self.pnl_ + new_position_ * self.current_price_ * self.numbers_to_dollars_
                    if self.total_pnl_ < self.min_pnl_till_now_ :
                        self.min_pnl_till_now_ = self.total_pnl_
                    self.opentrade_unrealized_pnl_ = self.total_pnl_ - self.realized_pnl_
            else :
                self.pnl_ += abs_change_position_ * _price_ * self.numbers_to_dollars_
                self.pnl_ -= abs_change_position_ * self.commish_dollars_per_unit_
                self.total_pnl_ = self.pnl_ + new_position_ * self.current_price_ * self.numbers_to_dollars_
                if self.total_pnl_ < self.min_pnl_till_now_ :
                    self.min_pnl_till_now_ = self.total_pnl_
                self.opentrade_unrealized_pnl_ = self.total_pnl_ - self.realized_pnl_
                self.average_open_price_ = (self.average_open_price_ * self.position_ + _price_* (new_position_ - self.position_))/new_position_
        self.position_ = new_position_                
    
    def LogTrade(self):
        return