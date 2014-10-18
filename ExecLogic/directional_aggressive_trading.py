from ExecLogic.base_trading import BaseTrading

class DirectionalAggressiveTrading(BaseTrading):
    
    def __init__(self, _watch_, _dep_market_view_, _order_manager_, _paramfilename_, _trading_start_time_, 
                 _trading_end_time_, _runtime_id_, _model_source_shortcode_vec_):
        super(DirectionalAggressiveTrading, self).__init__(_watch_, _dep_market_view_, _order_manager_, _paramfilename_, _trading_start_time_, 
                 _trading_end_time_, _runtime_id_, _model_source_shortcode_vec_)
        
    def __del__(self):
        return
    
    def StrategyName(self):
        return 'DirectionalAggressiveTrading'
    
    def TradingLogic(self):

        self.top_bid_place_ = False
        self.top_bid_keep_ = False
        self.top_bid_improve_ = False
        self.top_ask_lift_ = False
        self.bid_improve_keep_ = False

        if (self.current_tradevarset_.l1bid_trade_size_ == 0):
            return #not return correct this
        if ((self.last_buy_msecs_ > 0) and 
            (self.watch_.msecs_from_midnight() - self.last_buy_msecs_ < self.param_set_.cooloff_interval_)):
            pass
        else:
            if ((self.best_nonself_bid_size_ > self.param_set_.safe_distance) or 
                (self.targetbias_numbers_ >= self.current_tradevarset_.l1bid_place_)):
                self.top_bid_place_ = True
                self.top_bid_keep_ = True
                
                if (self.watch_.msecs_from_midnight() - self.last_agg_buy_msecs_ > self.param_set_.agg_cooloff_interval_):
                    
                    if ((self.param_set_.allowed_to_aggress_) and 
                        (self.targetbias_numbers_ >= self.current_tradevarset_.l1bid_aggressive_) and 
                        (self.my_position_ <= self.param_set_.max_position_to_lift_ ) and
                        (self.dep_market_view_.spread_increments() <= self.param_set_.max_int_spread_to_cross_)):
                        self.top_ask_lift_ = True

                        if (self.my_position_ >= self.param_set_.max_position_to_cancel_on_lift_):
                            self.top_bid_place_ = False
                            self.top_bid_keep_ = False
                    else:
                        self.top_ask_lift_ = False
                        
                        if ((self.param_set_.allowed_to_improve_) and 
                            (self.targetbias_numbers_ >= self.current_tradevarset_.l1bid_improve_) and 
                            (self.my_position_ <= self.param_set_.max_position_to_bidimprove_) and 
                            (self.dep_market_view_.spread_increments() >= self.param_set_.min_int_spread_to_improve_)):
                            self.top_bid_improve_ = True
                        else:
                            self.top_bid_improve_ = False
            else:
                if (self.targetbias_numbers_ >= self.current_tradevarset_.l1bid_keep_):
                    self.top_bid_keep_ = True
                else:
                    self.top_bid_keep_ = False

                if ((self.dep_market_view_.spread_increments() > 1 ) and
                    (self.targetbias_numbers_ >= self.current_tradevarset_.l1bid_improve_keep_)):
                    self.bid_improve_keep_ = True
                else:
                    self.bid_improve_keep_ = False

        self.top_ask_place_ = False
        self.top_ask_keep_ = False
        self.top_ask_improve_ = False
        self.top_bid_hit_ = False
        self.ask_improve_keep_ = False

        if (self.current_tradevarset_.l1ask_trade_size_ == 0):
            return #not return correct this
        if ((self.last_sell_msecs_ > 0) and 
            (self.watch_.msecs_from_midnight( ) - self.last_sell_msecs_ < self.param_set_.cooloff_interval_)):
            pass
        else:
            if ((self.best_nonself_ask_size_ > self.param_set_.safe_distance_) or 
                (-self.targetbias_numbers_ >= self.current_ask_tradevarset_.l1ask_place_)):
                self.top_ask_place_ = True
                self.top_ask_keep_ = True
                
                if (self.watch_.msecs_from_midnight() - self.last_agg_sell_msecs_ > self.param_set_.agg_cooloff_interval_):
                    
                    if ((self.param_set_.allowed_to_aggress_) and 
                        (self.my_position_ >= self.param_set_.min_position_to_hit_) and 
                        (self.best_nonself_ask_int_price_ - self.best_nonself_bid_int_price_ <= self.param_set_.max_int_spread_to_cross_) and 
                        (-self.targetbias_numbers_ >= self.current_tradevarset_.l1ask_aggressive_)):
                        self.top_bid_hit_ = True

                        if (self.my_position_ <= self.param_set_.min_position_to_cancel_on_hit_):
                            self.top_ask_place_ = False
                            self.top_ask_keep_ = False
                    else:
                        self.top_bid_hit_ = False
                        
                        if ((self.param_set_.allowed_to_improve_) and 
                            (self.my_position_ <= self.param_set_.min_position_to_askimprove_) and 
                            (self.dep_market_view_.spread_increments() >= self.param_set_.min_int_spread_to_improve_) and 
                            (self.targetbias_numbers_ >= self.current_tradevarset_.l1ask_improve_)):
                            self.top_ask_improve_ = True
                        else:
                            self.top_ask_improve_ = False
            else:
                if (- self.targetbias_numbers_ >= self.current_tradevarset_.l1ask_keep_):
                    self.top_ask_keep_ = True
                else:
                    self.top_ask_keep_ = False
                
                if ((self.dep_market_view_.spread_increments() > 1) and 
                    (- self.targetbias_numbers_ >= self.current_tradevarset_.l1ask_improve_keep_)):
                    self.ask_improve_keep_ = True
                else:
                    self.ask_improve_keep_ = False

        placed_bids_this_round_ = False
        canceled_bids_this_round_ = False
        canceled_size_ = 0
        
        if (self.top_ask_lift_):
            if ((self.order_manager_.SumBidSizeUnconfirmedEqAboveIntPrice(self.best_nonself_bid_int_price_+1) == 0) and 
                (self.order_manager_.SumBidSizeConfirmedAboveIntPrice(self.best_nonself_bid_int_price_) == 0)):
                if (not self.top_bid_keep_):
                    canceled_size_ += self.order_manager_.CancelBidsEqAboveIntPrice(self.best_nonself_bid_int_price_)
                
                allowance_for_aggressive_buy_ = self.my_position_ + self.order_manager_.SumBidSizes() + self.current_tradevarset_.l1bid_trade_size_ - self.param_set_.worst_case_position_
                if (allowance_for_aggressive_buy_ >= 0):
                    if (allowance_for_aggressive_buy_ > canceled_size_):
                        canceled_size_ += self.order_manager_.CancelBidsFromFar(self.current_tradevarset_.l1bid_trade_size_)
                else:
                    self.order_manager_.SendTrade(self.best_nonself_ask_price_, self.best_nonself_ask_int_price_, 
                                                  self.current_tradevarset_.l1bid_trade_size_, 0, 'A' ) # 0 => Buy
                    placed_bids_this_round_ = True
                    self.last_agg_buy_msecs_ = self.watch_.msecs_from_midnight()
                    self.last_buy_msecs_ = self.watch_.mecs_from_midnight()
            else:
                canceled_size_ += self.order_manager_.CancelBidsAboveIntPrice(self.best_nonself_bid_int_price_)
    
        if ((not placed_bids_this_round_) and (self.top_bid_improve_)):
            if ((self.order_manager_.SumBidSizeUnconfirmedEqAboveIntPrice(self.best_nonself_bid_int_price_ + 1) == 0) and 
                (self.order_manager_.SumBidSizeConfirmedAboveIntPrice(self.best_nonself_bid_int_price_) == 0)):

                if (self.my_position_ + self.order_manager_.SumBidSizes() + self.current_tradevarset_.l1bid_trade_size_ >= self.param_set_.worst_case_position_ ):
                    canceled_size_ += self.order_manager_.CancelBidsFromFar(self.current_tradevarset_.l1bid_trade_size_)
                else:
                    self.order_manager_.SendTradeIntPx((self.best_nonself_bid_int_price_ + 1), self.current_tradevarset_.l1bid_trade_size_, 0, 'A')
                    placed_bids_this_round_ = True
                    self.last_agg_buy_msecs_ = self.watch_.msecs_from_midnight()
                    self.last_buy_msecs_ = self.watch_.msecs_from_midnight()
        else:
            if ((self.dep_market_view_.spread_increments() > 1) and (not self.bid_improve_keep_)):
                canceled_size_ += self.order_manager_.CancelBidsAboveIntPrice(self.best_nonself_bid_int_price_)
    
        if (not placed_bids_this_round_):
            if (self.top_bid_place_):
                if ((self.order_manager_.SumBidSizeUnconfirmedEqAboveIntPrice(self.best_nonself_bid_int_price_) == 0) and
                    (self.order_manager_.SumBidSizeConfirmedEqAboveIntPrice(self.best_nonself_bid_int_price_) == 0) and 
                    (self.dep_market_view_.spread_increments() <= self.param_set_.max_int_spread_to_place_)):
                    self.order_manager_.SendTrade(self.best_nonself_bid_price_, self.best_nonself_bid_int_price_, self.current_tradevarset_.l1bid_trade_size_, 0, 'B')
                    placed_bids_this_round_ = True
                    self.last_buy_msecs_ = self.watch_.msecs_from_midnight()
            else:
                if (not self.top_bid_keep_):
                    canceled_size_ += self.order_manager_.CancelBidsEqAboveIntPrice(self.best_nonself_bid_int_price_)
    
        if (canceled_size_ > 0):
            canceled_bids_this_round_ = True

        placed_asks_this_round_ = False
        canceled_asks_this_round_ = False
        canceled_size_ = 0

        if (self.top_bid_hit_):

            if ((self.order_manager_.SumAskSizeUnconfirmedEqAboveIntPrice(self.best_nonself_ask_int_price_ - 1) == 0) and 
                (self.order_manager_.SumAskSizeConfirmedAboveIntPrice(self.best_nonself_ask_int_price_) == 0)):
                if (not self.top_ask_keep_):
                    canceled_size_ += self.order_manager_.CancelAsksEqAboveIntPrice(self.best_nonself_ask_int_price_)
                allowance_for_aggressive_sell_ = - self.my_position_ + self.order_manager_.SumAskSizes() + self.current_tradevarset_.l1ask_trade_size_ - self.param_set_.worst_case_position_
                if (allowance_for_aggressive_sell_ >= 0):
                    if (allowance_for_aggressive_sell_ > canceled_size_):
                        canceled_size_ += self.order_manager_.CancelAsksFromFar(self.current_tradevarset_.l1ask_trade_size_)
                else:
                    self.order_manager_.SendTrade(self.best_nonself_bid_price_, self.best_nonself_bid_int_price_, self.current_tradevarset_.l1ask_trade_size_, 1, 'A') # 1 => Sell
                    placed_asks_this_round_ = True
                    self.last_agg_sell_msecs_ = self.watch_.msecs_from_midnight()
                    self.last_sell_msecs_ = self.watch_.msecs_from_midnight()
            else:
                canceled_size_ += self.order_manager_.CancelAsksAboveIntPrice(self.best_nonself_ask_int_price_)
    
        if ((not placed_asks_this_round_) and (self.top_ask_improve_)):

            if ((self.order_manager_.SumAskSizeUnconfirmedEqAboveIntPrice(self.best_nonself_ask_int_price_ - 1) == 0) and 
                (self.order_manager_.SumAskSizeConfirmedAboveIntPrice(self.best_nonself_ask_int_price_) == 0)):
                if (- self.my_position_ + self.order_manager_.SumAskSizes() + self.current_tradevarset_.l1ask_trade_size_ >= self.param_set_.worst_case_position_):
                    canceled_size_ += self.order_manager_.CancelAsksFromFar(self.current_tradevarset_.l1ask_trade_size_)
                else:
                    self.order_manager_.SendTradeIntPx((self.best_nonself_ask_int_price_ - 1), self.current_tradevarset_.l1ask_trade_size_, 1, 'A' )
                    placed_asks_this_round_ = True
                    self.last_agg_sell_msecs_ = self.watch_.msecs_from_midnight()
                    self.last_sell_msecs_ = self.watch_.msecs_from_midnight()
        else:
            if ((self.dep_market_view_.spread_increments() > 1) and (not self.ask_improve_keep_)): 
                canceled_size_ += self.order_manager_.CancelAsksAboveIntPrice(self.best_nonself_ask_int_price_)
    
        if (not placed_asks_this_round_):
            if (self.top_ask_place_):
                if ((self.order_manager_.SumAskSizeUnconfirmedEqAboveIntPrice(self.best_nonself_ask_int_price_) == 0) and 
                    (self.order_manager_.SumAskSizeConfirmedEqAboveIntPrice(self.best_nonself_ask_int_price_) == 0) and 
                    (self.dep_market_view_.spread_increments() <= self.param_set_.max_int_spread_to_place_)):
                    self.order_manager_.SendTrade(self.best_nonself_ask_price_, self.best_nonself_ask_int_price_, self.current_tradevarset_.l1ask_trade_size_, 1, 'B')
                    placed_asks_this_round_ = True
                    self.last_sell_msecs_ = self.watch_.msecs_from_midnight()
            else:
                if (not self.top_ask_keep_ ):
                    canceled_size_ += self.order_manager_.CancelAsksEqAboveIntPrice(self.best_nonself_ask_int_price_)
        
        if (canceled_size_ > 0):
            canceled_asks_this_round_ = True
            
        if (placed_bids_this_round_ or placed_asks_this_round_ or canceled_bids_this_round_ or canceled_asks_this_round_):
            dump_inds = True