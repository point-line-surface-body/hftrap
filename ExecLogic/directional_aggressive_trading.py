from ExecLogic.base_trading import BaseTrading

class DirectionalAggressiveTrading(BaseTrading):
    
    # Not handling:
    # (1) Economic Events
    
    # List out the variables used
    # best_nonself_bid_int_price_
    # best_nonself_ask_int_price_
    # my_position_
    # param_set_
    # current_tradevarset_
    
    def __init__(self, _watch_, _dep_market_view_, _order_manager_, _paramfilename_, _trading_start_time_, 
                 _trading_end_time_, _runtime_id_, _model_source_shortcode_vec_):
        BaseTrading.__init__(_watch_, _dep_market_view_, _order_manager_, _paramfilename_, _trading_start_time_, 
                 _trading_end_time_, _runtime_id_, _model_source_shortcode_vec_)
        
    def __del__(self):
        return
    
    def StrategyName(self):
        return 'DirectionalAggressiveTrading'
    
    def TradingLogic(self):
        # Maximum number of orders we can place at one go
        num_max_orders_ = 1
        # Current number of unconfirmed orders
        our_bid_orders_ = self.order_manager_.SumBidSizeUnconfirmedEqAboveIntPrice(self.best_nonself_bid_int_price_)+self.order_manager_.SumBidSizeConfirmedEqAboveIntPrice(self.best_nonself_bid_int_price_)
        our_ask_orders_ = self.order_manager_.SumAskSizeUnconfirmedEqAboveIntPrice(self.best_nonself_ask_int_price_)+self.order_manager_.SumAskSizeConfirmedEqAboveIntPrice(self.best_nonself_ask_int_price_)

        effective_bid_position_ = self.my_position_
        effective_ask_position_ = self.my_position_
        effective_bid_position_to_keep_ = self.my_position_
        effective_ask_position_to_keep_ = self.my_position_

#         if (param_set_.place_multiple_orders_):
#             num_max_orders_ = param_set_.max_unit_size_at_level_ ;
#             effective_bid_position_ = our_bid_orders_ + my_position_ - order_manager_.SumBidSizeCancelRequested ( best_nonself_bid_int_price_ ) ;
#             effective_ask_position_ =  - our_ask_orders_ + my_position_ + order_manager_.SumAskSizeCancelRequested ( best_nonself_ask_int_price_ ) ;
#             effective_bid_position_to_keep_ = effective_bid_position_ - current_tradevarset_.l1bid_trade_size_ ;
#             effective_ask_position_to_keep_ = effective_ask_position_ + current_tradevarset_.l1ask_trade_size_ ;

        # setting top level directives
        top_bid_place_ = False
        top_bid_keep_ = False
        top_bid_improve_ = False
        top_ask_lift_ = False
        bid_improve_keep_ = False

        # if based on current risk level or if trading is stopped ... check if we have any allowance to place orders at top level
        if (self.current_tradevarset_.l1bid_trade_size_ == 0):
            return
        # first check for cooloff_interval (why the second condition?)
        if ((self.last_buy_msecs_ > 0) and (self.watch_.msecs_from_midnight()-self.last_buy_msecs_ < self.param_set_.cooloff_interval_) and (best_nonself_bid_int_price_ >= last_buy_int_price_)):
            # no bids at this or higher prices now
            pass
        else:
            # check if the margin of buying i.e. ( targetbias_numbers_ ) exceeds the threshold current_tradevarset_.l1bid_place_
            if ((self.best_nonself_bid_size_ > self.param_set_.safe_distance) or 
                ((self.targetbias_numbers_+((self.dep_market_view_.spread_increments() > self.moving_avg_dep_bidask_spread_) ? (self.param_set_.high_spread_allowance_) : 0.0) >= self.position_tradevarset_map_[self.GetPositonToTradeVarsetMapIndex(self.effective_bid_position_)].l1bid_place_-self.l1_bias_-self.l1_order_bias_-self.short_positioning_bias_) and
                 (self.best_nonself_bid_size_ > self.param_set_.min_size_to_join_) and 
                 (self.param_set_.place_on_trade_update_implied_quote_ or not self.dep_market_view_.trade_update_implied_quote()))):
                top_bid_place_ = True
                top_bid_keep_ = True
                if (self.watch_.msecs_from_midnight()-self.last_agg_buy_msecs_ > self.param_set_.agg_cooloff_interval_):
                    # aggressive and improve
                    if ((self.param_set_.allowed_to_aggress_) and 
                        (self.targetbias_numbers_ >= self.current_tradevarset_.l1bid_aggressive_) and 
                        # only LIFT offer if the margin of buying exceeds the threshold
                        (self.current_tradevarset_.l1bid_aggressive_(self.my_position_ <= param_set_.max_position_to_lift_ ) and
                        # Don't LIFT offer when my_position_ is already decently long
                        (self.dep_market_view_.spread_increments() <= param_set_.max_int_spread_to_cross_) and
                        # Don't LIFT when effective spread is too much
                        # TODO_OPT : later change setting of last_buy_int_price_ to include px_band_
                        ((self.last_buy_msecs_ <= 0 ) or (self.watch_.msecs_from_midnight()-self.last_buy_msecs_ >= self.param_set_.cooloff_interval_) or ((self.best_nonself_ask_int_price_-self.last_buy_int_price_ ) < (self.param_set_.px_band_-1)))):
                        top_ask_lift_ = True
                        # when we are already long and ask_lift is set to true, place and keep at top bid are set false so that
                        # we cancel top level orders before we place new ones at aggressive prices
                        if (self.my_position_ >= self.param_set_.max_position_to_cancel_on_lift_):
                            top_bid_place_ = False
                            top_bid_keep_ = False
                    else:
                        top_ask_lift_ = False
                        # conditions to place market improving bid orders:
                        # ALLOWED_TO_IMPROVE
                        # position is not too long already
                        # spread wide
                        # signal strong
                        if ((self.param_set_.allowed_to_improve_) and 
                            (self.my_position_ <= self.param_set_.max_position_to_bidimprove_) and 
                            # Don't improve bid when my_position_ is already decently long
                            (self.dep_market_view_.spread_increments() >= self.param_set_.min_int_spread_to_improve_) and 
                            (self.targetbias_numbers_ >= self.current_tradevarset_.l1bid_improve_) and 
                            ((self.last_buy_msecs_ <= 0) or (self.watch_.msecs_from_midnight()-self.last_buy_msecs_ >= self.param_set_.cooloff_interval_) or (((self.best_nonself_bid_int_price_+1)-self.last_buy_int_price_) < (self.param_set_.px_band_-1)))
                            # TODO_OPT : later change setting of last_buy_int_price_ to include px_band_)
                            top_bid_improve_ = True
                        else:
                            top_bid_improve_ = False
            else:
                # signal is not strong enough for placing bids at best_nonself_bid_price_
                # check if we should retain exisiting bids due to place_in_line
                # TODO : perhaps we should make place_in_line effect bestbid_queue_hysterisis_ smarter
                #        for instance when short term volatility in the market is very high
                #        then being high in the queue should count for less.
                if ((self.targetbias_numbers_+((self.dep_market_view_.spread_increments() > self.moving_avg_dep_bidask_spread_) ? (self.param_set_.high_spread_allowance_) : 0.0)+self.bestbid_queue_hysterisis_) >= self.position_tradevarset_map_[self.GetPositonToTradeVarsetMapIndex(self.effective_bid_position_to_keep_)].l1bid_keep_-self.l1_bias_-self.short_positioning_bias_-self.l1_order_bias_):
                    top_bid_keep_ = True
                else
                    top_bid_keep_ = False
                if ((self.dep_market_view_.spread_increments() > 1 ) and
                    (self.targetbias_numbers_+((self.dep_market_view_.spread_increments() > self.moving_avg_dep_bidask_spread_) ? (self.param_set_.high_spread_allowance_) : 0.0)+self.bestbid_queue_hysterisis_) >= self.current_tradevarset_.l1bid_improve_keep_-self.l1_bias_-self.short_positioning_bias_-self.l1_order_bias_):
                    bid_improve_keep_ = True
                else:
                    bid_improve_keep_ = False

        if ( ( param_set_.read_primary_ors_indicator_ &&  param_set_.read_primary_ors_indicator_cancel_threshold_ && primary_ors_indicator_bias_ < - param_set_.primary_ors_indicator_cancel_threshold_ ) ||( param_set_.read_secondary_ors_indicator_ && param_set_.read_secondary_ors_indicator_ && secondary_ors_indicator_bias_ < - param_set_.secondary_ors_indicator_cancel_threshold_ ) )
            self.cancel_bid_on_ors_message_ = True

        if ( ( param_set_.read_primary_ors_indicator_ && primary_ors_indicator_bias_ < -param_set_.primary_ors_indicator_all_cancel_threshold_ ) ||( param_set_.read_secondary_ors_indicator_ && secondary_ors_indicator_bias_ < -param_set_.secondary_ors_indicator_all_cancel_threshold_ ) )
            self.order_manager_.CancelBidsEqAboveIntPrice ( best_nonself_bid_int_price_ + (int) primary_ors_indicator_bias_ + 1 );

        top_ask_place_ = False
        top_ask_keep_ = False
        top_ask_improve_ = False
        top_bid_hit_ = False
        ask_improve_keep_ = False

        # if based on current risk level or if trading is stopped ... check if we have any allowance to place orders at top level
        if ( 
            # check if we have any allowance to place orders at top level ( current_tradevarset_.l1ask_trade_size_ > 0 ) && // first check for cooloff_interval ( ( last_sell_msecs_ <= 0 ) || ( watch_.msecs_from_midnight( ) - last_sell_msecs_ >= param_set_.cooloff_interval_ ) ||  ( last_sell_int_price_ - best_nonself_ask_int_price_ < ( param_set_.px_band_ - 1 ) ) ) // later change setting of last_sell_int_price_ to include px_band_)
    {
        # check if the margin of placing limit ask orders at the price ( best_nonself_ask_price_ )
        # i.e. ( best_nonself_ask_price_ - target_price_ )
        #      exceeds the threshold current_tradevarset_.l1ask_place_

        if ( ( best_nonself_ask_size_ > param_set_.safe_distance_ ) || ( ( ( -targetbias_numbers_ + ( ( dep_market_view_.spread_increments() > 1 ) ? ( param_set_.high_spread_allowance_ ) : 0.0 ) ) >= position_tradevarset_map_ [ (  GetPositonToTradeVarsetMapIndex ( effective_ask_position_ ) ) ].l1ask_place_ - l1_bias_ - long_positioning_bias_ - l1_order_bias_ ) &&( best_nonself_ask_size_ > param_set_.min_size_to_join_ ) && ( param_set_.place_on_trade_update_implied_quote_ || ! dep_market_view_.trade_update_implied_quote ( ) ) ) )
        {
            top_ask_place_ = true ;
            top_ask_keep_ = true ;

            if ( watch_.msecs_from_midnight () - last_agg_sell_msecs_ > param_set_.agg_cooloff_interval_ )
            {
                # aggressive and improve */
                # conditions to place aggressive orders:
                # ALLOWED_TO_AGGRESS
                # position is not too short already
                # spread narrow
                # signal strong
                if ( ( param_set_.allowed_to_aggress_ ) && /* external control on aggressing */ ( my_position_ >= param_set_.min_position_to_hit_ ) && /* Don't HIT bid when my_position_ is already decently short */( best_nonself_ask_int_price_ - best_nonself_bid_int_price_ <= param_set_.max_int_spread_to_cross_ ) && /* Don't HIT ( cross ) when effective spread is to much */( -targetbias_numbers_ >= current_tradevarset_.l1ask_aggressive_ ) &&( ( last_sell_msecs_ <= 0 ) ||( watch_.msecs_from_midnight( ) - last_sell_msecs_ >= param_set_.cooloff_interval_ ) ||( ( last_sell_int_price_ - best_nonself_bid_int_price_ ) < ( param_set_.px_band_ - 1 ) ) ) // TODO_OPT : later change setting of last_sell_int_price_ to include px_band_)
                {

                    top_bid_hit_ = true ;

                    /* when we are already short and bit_hit is set to true,
                    place and keep at top ask are set false so that
                    we cancel top level orders before we place new ones at aggressive prices */
                    if ( my_position_ <= param_set_.min_position_to_cancel_on_hit_ )
                    {
                        top_ask_place_ = false ;
                        top_ask_keep_ = false ;
                    }
                }
                else
                {
                    top_bid_hit_ = false ;
                    if ( ( param_set_.allowed_to_improve_ ) && ( my_position_ >= param_set_.min_position_to_askimprove_ ) && /* Don't improve ask when my_position_ is already decently short */( best_nonself_ask_int_price_ - best_nonself_bid_int_price_ >= param_set_.min_int_spread_to_improve_ ) &&( targetbias_numbers_ >= current_tradevarset_.l1ask_improve_ ) &&( ( last_sell_msecs_ <= 0 ) ||( watch_.msecs_from_midnight( ) - last_sell_msecs_ >= param_set_.cooloff_interval_ ) ||( ( (last_sell_int_price_ - 1) - best_nonself_ask_int_price_ ) < ( param_set_.px_band_ - 1 ) ) ) // TODO_OPT : later change setting of last_sell_int_price_ to include px_band_)
                    {
                        top_ask_improve_ = true ;
                    }
                    else
                    {
                        top_ask_improve_ = false ;
                    }
                }
            }
        }
        else
        {
            # signal not strog enough to place limit orders at the best ask level
            if ( ( -targetbias_numbers_ + ( ( dep_market_view_.spread_increments() > moving_avg_dep_bidask_spread_ ) ? ( param_set_.high_spread_allowance_ ) : 0.0 ) + bestask_queue_hysterisis_ ) >= position_tradevarset_map_[  GetPositonToTradeVarsetMapIndex ( effective_ask_position_to_keep_)].l1ask_keep_ - l1_bias_ - l1_order_bias_ - long_positioning_bias_ )
            { // but with place in line effect enough to keep the live order there
                top_ask_keep_ = true ;
            }
            else
            {
                top_ask_keep_ = false ;
            }
        }
        if ( ( dep_market_view_.spread_increments () > 1 ) && ( -targetbias_numbers_ + ( ( dep_market_view_.spread_increments () > moving_avg_dep_bidask_spread_ ) ? ( param_set_.high_spread_allowance_ ) : 0.0 ) + bestask_queue_hysterisis_ ) >= current_tradevarset_.l1ask_improve_keep_ - l1_bias_ - l1_order_bias_ - long_positioning_bias_ )
        {
            ask_improve_keep_ = true;
        }
        else
        {
            ask_improve_keep_ = false;
        }
    }


    if ( ( param_set_.read_primary_ors_indicator_ &&  param_set_.read_primary_ors_indicator_cancel_threshold_ && primary_ors_indicator_bias_ > param_set_.primary_ors_indicator_cancel_threshold_ ) ||( param_set_.read_secondary_ors_indicator_ && param_set_.read_secondary_ors_indicator_cancel_threshold_ && secondary_ors_indicator_bias_ > param_set_.secondary_ors_indicator_cancel_threshold_  ))
    {
        cancel_ask_on_ors_message_ = true;
    }

    if ( (  param_set_.read_primary_ors_indicator_ && primary_ors_indicator_bias_ > param_set_.primary_ors_indicator_all_cancel_threshold_ ) ||(  param_set_.read_secondary_ors_indicator_ && secondary_ors_indicator_bias_ > param_set_.secondary_ors_indicator_all_cancel_threshold_ ) )
    {
        order_manager_.CancelAsksEqAboveIntPrice ( best_nonself_ask_int_price_  + (int)primary_ors_indicator_bias_ + 1 ) ;
    }

    if ( called_on_ors_message_ )
    {
        top_bid_place_ = false;
        top_ask_lift_ = false;
        top_ask_place_ = false;
        top_bid_hit_ = false;
        top_bid_keep_ = true;
        top_ask_keep_ = true;
    }

    if (called_on_ors_message_ && !cancel_bid_on_ors_message_ && !cancel_ask_on_ors_message_ )
    {
        called_on_ors_message_ = false;
        return;
    }
    else if ( called_on_ors_message_ && cancel_bid_on_ors_message_ )
    {
        cancel_bid_on_ors_message_ = false;
        top_bid_keep_ = false;
    }
    else if ( called_on_ors_message_ && cancel_ask_on_ors_message_ )
    {
        cancel_ask_on_ors_message_ = false;
        top_ask_keep_ = false;
    }

    called_on_ors_message_ = false;


    # After setting top-level directives ...
    # get to order placing or canceling part

    # Active BID rder management
    bool placed_bids_this_round_ = false;
    bool canceled_bids_this_round_ = false;
    if ( top_ask_lift_ )
    {
        # only place aggressive orders when there is no active unconfirmed order and no confirmed orders above the best price
        # and no confirmed orders above the best_nonself_bid_price_
        if ( ( order_manager_.SumBidSizeUnconfirmedEqAboveIntPrice ( best_nonself_bid_int_price_ + 1 ) == 0 ) && ( order_manager_.SumBidSizeConfirmedAboveIntPrice ( best_nonself_bid_int_price_ ) == 0 ) )
        {
            int _canceled_size_ = 0;
            if ( ! top_bid_keep_ )
            { 
                # if due to position placing aggressive LIFT order requires us to cancel bids from all active levels
                _canceled_size_ += order_manager_.CancelBidsEqAboveIntPrice ( best_nonself_bid_int_price_ ) ;
                if ( _canceled_size_ > 0 )
                {
                    canceled_bids_this_round_ = true;
                    if ( dbglogger_.CheckLoggingLevel  ( TRADING_INFO ) )
                    {
                        DBGLOG_TIME_CLASS_FUNC_LINE << " Cancelling bids eq above : " << best_nonself_bid_int_price_ << " Size: " << _canceled_size_ << DBGLOG_ENDL_FLUSH;
                    }
                }
            }
            int allowance_for_aggressive_buy_ = my_position_ + order_manager_.SumBidSizes ( ) +  current_tradevarset_.l1bid_trade_size_ - param_set_.worst_case_position_ ;
            if ( param_set_.use_new_aggress_logic_ )
            {
                allowance_for_aggressive_buy_ =  my_position_ + order_manager_.SumBidSizes ( ) + current_tradevarset_.l1bid_trade_size_ - std::max ( param_set_.worst_case_position_ , param_set_.max_position_ );
            }

            # if we are getting very close to worst_case_position_ with cnf and uncnf orders on the bid side
            if ( allowance_for_aggressive_buy_ >= 0 )
            {
                # and if size canceled already is less than l1bid_trade_size_
                if ( allowance_for_aggressive_buy_ > _canceled_size_ )
                {
                    # then cancel Bids from bottom levels for the required size
                    _canceled_size_ += order_manager_.CancelBidsFromFar ( current_tradevarset_.l1bid_trade_size_ );
  
                    if ( dbglogger_.CheckLoggingLevel  ( TRADING_INFO ) )
                    {
                        DBGLOG_TIME_CLASS_FUNC_LINE << " Cancelling bids eq above : " << best_nonself_bid_int_price_ <<" Size: "  << _canceled_size_ << DBGLOG_ENDL_FLUSH;
                    }
                }
            }
            else
            {
                # Place new order */
                order_manager_.SendTrade ( best_nonself_ask_price_, best_nonself_ask_int_price_, current_tradevarset_.l1bid_trade_size_, kTradeTypeBuy, 'A' ) ;
                placed_bids_this_round_ = true;
                last_agg_buy_msecs_ = watch_.msecs_from_midnight();
            }
        }
        else
        {
            int canceled_size_ = order_manager_.CancelBidsAboveIntPrice ( best_nonself_bid_int_price_ ) ; // only after canceling them can we be allowed to place aggressive orders
            if ( dbglogger_.CheckLoggingLevel  ( TRADING_INFO ) )
            {
                DBGLOG_TIME_CLASS_FUNC_LINE << " Cancelling bids eq above : " << best_nonself_bid_int_price_ << " Size: " << canceled_size_ <<  DBGLOG_ENDL_FLUSH;
            }
        }
    }

    if ( ( ! placed_bids_this_round_ ) && ( top_bid_improve_ ) )
    {
        # only place Bid Improve orders when there is no active unconfirmed order and no confirmed orders above the best price
        if ( ( order_manager_.SumBidSizeUnconfirmedEqAboveIntPrice ( best_nonself_bid_int_price_ + 1 ) == 0 ) && ( order_manager_.SumBidSizeConfirmedAboveIntPrice ( best_nonself_bid_int_price_ ) == 0 ) )
        {
            # if we are getting very close to worst_case_position_ with cnf and uncnf orders on the bid side
            if ( my_position_ + order_manager_.SumBidSizes ( ) + current_tradevarset_.l1bid_trade_size_ >= param_set_.worst_case_position_ )
            {
                int _canceled_size_ = 0;
                # then cancel Bids from bottom levels for the required size
                _canceled_size_ += order_manager_.CancelBidsFromFar ( current_tradevarset_.l1bid_trade_size_ );

                if ( dbglogger_.CheckLoggingLevel  ( TRADING_INFO ) )
                {
                    DBGLOG_TIME_CLASS_FUNC_LINE << " Cancelling bids eq above : " << best_nonself_bid_int_price_ <<" Size: "  << _canceled_size_ << DBGLOG_ENDL_FLUSH;
                }
            }
            else
            {
                # Place new order */
                order_manager_.SendTradeIntPx ( (best_nonself_bid_int_price_ + 1), current_tradevarset_.l1bid_trade_size_, kTradeTypeBuy, 'A' ) ;
                last_agg_buy_msecs_ = watch_.msecs_from_midnight();
                placed_bids_this_round_ = true;
                if ( dbglogger_.CheckLoggingLevel ( TRADING_INFO ) ) //zero logging
                {
                    DBGLOG_TIME_CLASS_FUNC << "Sending improve B at px " << best_nonself_bid_int_price_ +1 << " position " << my_position_ << DBGLOG_ENDL_FLUSH ;
                }
            }
        }
    }
    else
    {
        if ( ( dep_market_view_.spread_increments () > 1 ) && ( ! bid_improve_keep_ ) ) // can have size check here for optimization purpose
        {
            int cancelled_size_ = order_manager_.CancelBidsAboveIntPrice  ( best_nonself_bid_int_price_ ) ;
            if ( cancelled_size_ > 0 )
            {
                if ( dbglogger_.CheckLoggingLevel ( TRADING_INFO ) )
                {
                    DBGLOG_TIME_CLASS_FUNC << " Cancelled Improve Bid orders Above: " << best_nonself_bid_int_price_ 
              << " Position: " << my_position_
              << " tgt_bias: " << targetbias_numbers_ / dep_market_view_.min_price_increment()
              << " thresh_t: " << current_tradevarset_.l1bid_improve_keep_ / dep_market_view_.min_price_increment()
              << DBGLOG_ENDL_FLUSH;
                }
            }
        }
    }

    if ( ! placed_bids_this_round_ )
    { 
        # only come here if no aggressive or improve bid orders sent this cycle
        if ( top_bid_place_ )
        {
            # only place Bid orders when there is no active unconfirmed order and no confirmed order at or above the best price
            if ( ( ( param_set_.place_multiple_orders_ &&
                     ( our_bid_orders_ < num_max_orders_ * param_set_.unit_trade_size_ ) &&
                     ( ( our_bid_orders_ + my_position_ + current_tradevarset_.l1bid_trade_size_ ) < param_set_.max_position_ ) ) ||
                   ( ( order_manager_.SumBidSizeUnconfirmedEqAboveIntPrice ( best_nonself_bid_int_price_ ) == 0 ) &&
             ( order_manager_.SumBidSizeConfirmedEqAboveIntPrice ( best_nonself_bid_int_price_ ) == 0 ) ) ) && 
                ( stdev_ <= param_set_.low_stdev_lvl_ || ( dep_market_view_.spread_increments() <= param_set_.max_int_spread_to_place_ ) ) ) // Don't place any new orders in inside market if the spread is too wide
            {
                order_manager_.SendTrade ( best_nonself_bid_price_, best_nonself_bid_int_price_, current_tradevarset_.l1bid_trade_size_, kTradeTypeBuy, 'B' ) ;
                if ( dbglogger_.CheckLoggingLevel ( TRADING_INFO ) )  //zero logging
                {
                    DBGLOG_TIME_CLASS_FUNC
                      << "SendTrade B of " << current_tradevarset_.l1bid_trade_size_ << " @ " << best_nonself_bid_price_
                      << " tgt_bias: " << targetbias_numbers_ / dep_market_view_.min_price_increment()
                      << " thresh_t: " << position_tradevarset_map_[ GetPositonToTradeVarsetMapIndex ( effective_bid_position_ ) ].l1bid_place_ / dep_market_view_.min_price_increment()
                      << " Int Px: " << best_nonself_bid_int_price_
                      << " tMktSz: " << best_nonself_bid_size_
                      << " Mkt: " << best_nonself_bid_size_ << " @ " << best_nonself_bid_price_ << "  ---  " << best_nonself_ask_price_ << " @ " << best_nonself_ask_size_
                      << DBGLOG_ENDL_FLUSH;
                }
            }
        }
        else
        {
            if ( ! top_bid_keep_ )
            { 
                # cancel all orders at best_nonself_bid_price_
                int canceled_size_ = 0;
                if ( param_set_.place_multiple_orders_ ) 
                {
                    canceled_size_ = order_manager_.CancelBidsEqAboveIntPrice ( best_nonself_bid_int_price_, param_set_.unit_trade_size_) ;
                }
                else
                {
                    canceled_size_ = order_manager_.CancelBidsEqAboveIntPrice ( best_nonself_bid_int_price_ ) ;
                }
                if ( canceled_size_ > 0 )
                {
                    canceled_bids_this_round_ = true;
                    if ( dbglogger_.CheckLoggingLevel ( TRADING_INFO ) ) //zero logging
                    {
                        DBGLOG_TIME
                          << "Canceled B of " << canceled_size_ << " EqAbove " << best_nonself_bid_price_
                          << " tgt_bias: " << targetbias_numbers_ / dep_market_view_.min_price_increment()
                          << " thresh_t: " << position_tradevarset_map_ [ GetPositonToTradeVarsetMapIndex ( effective_bid_position_to_keep_ ) ].l1bid_keep_ / dep_market_view_.min_price_increment()
                          << " tMktSz: " << best_nonself_bid_size_
                          << DBGLOG_ENDL_FLUSH;
                    }
                }
            }
        }
    }



    # Active ASK order management
    bool placed_asks_this_round_ = false;
    bool canceled_asks_this_round_ = false;
    if ( top_bid_hit_ )
    {
        # only place aggressive orders when there is no active unconfirmed order and no confirmed orders above the best price
        if ( ( order_manager_.SumAskSizeUnconfirmedEqAboveIntPrice ( best_nonself_ask_int_price_ - 1 ) == 0 ) && ( order_manager_.SumAskSizeConfirmedAboveIntPrice ( best_nonself_ask_int_price_ ) == 0 ) )
        {
            int _canceled_size_ = 0;
            if ( ! top_ask_keep_ )
            { 
                # if due to position placing aggressive LIFT order requires us to cancel asks from all active levels
                _canceled_size_ += order_manager_.CancelAsksEqAboveIntPrice ( best_nonself_ask_int_price_ ) ;
            }
            int allowance_for_aggressive_sell_ = - my_position_ + order_manager_.SumAskSizes ( ) + current_tradevarset_.l1ask_trade_size_ - param_set_.worst_case_position_ ;
            if ( param_set_.use_new_aggress_logic_ )
            {
                allowance_for_aggressive_sell_ = - my_position_ + order_manager_.SumAskSizes ( ) + current_tradevarset_.l1ask_trade_size_ - std::max ( param_set_.max_position_ , param_set_.max_position_ );
            }
            # if we are getting very close to worst_case_position_ with cnf and uncnf orders on the ask side
            if ( allowance_for_aggressive_sell_ >= 0 )
            {
                # and if size canceled already is less than l1ask_trade_size_
                if ( allowance_for_aggressive_sell_ > _canceled_size_  )
                {
                    _canceled_size_ += order_manager_.CancelAsksFromFar ( current_tradevarset_.l1ask_trade_size_ ); ///< then cancel Asks from bottom levels for the required size
                }
        }
        else
        {
            # Place new order */
            order_manager_.SendTrade ( best_nonself_bid_price_, best_nonself_bid_int_price_, current_tradevarset_.l1ask_trade_size_, kTradeTypeSell, 'A' ) ;
            placed_asks_this_round_ = true;
            last_agg_sell_msecs_ = watch_.msecs_from_midnight();
            if ( dbglogger_.CheckLoggingLevel ( TRADING_INFO ) ) //zero logging
            {
                DBGLOG_TIME_CLASS_FUNC
                  << "Sending aggressive S at px " << best_nonself_bid_int_price_
                  << " position " << my_position_
                  << DBGLOG_ENDL_FLUSH ;
            }
        }
    }
    else
    {
        order_manager_.CancelAsksAboveIntPrice ( best_nonself_ask_int_price_ ) ; // only after canceling them can we be allowed to place aggressive orders
    }
}

    if ( ( ! placed_asks_this_round_ ) && ( top_ask_improve_ ) )
    {
        # only place Ask Improve orders when there is no active unconfirmed order and no confirmed orders above the best price
        if ( ( order_manager_.SumAskSizeUnconfirmedEqAboveIntPrice ( best_nonself_ask_int_price_ - 1 ) == 0 ) && ( order_manager_.SumAskSizeConfirmedAboveIntPrice ( best_nonself_ask_int_price_ ) == 0 ) )
        {
            # if we are getting very close to worst_case_position_ with cnf and uncnf orders on the ask side
            if ( -my_position_ + order_manager_.SumAskSizes ( ) + current_tradevarset_.l1ask_trade_size_ >= param_set_.worst_case_position_ )
            {
                int _canceled_size_ = 0;
                _canceled_size_ += order_manager_.CancelAsksFromFar ( current_tradevarset_.l1ask_trade_size_ ); ///< then cancel Asks from bottom levels for the required size
            }
            else
            {
                /* Place new order */
                order_manager_.SendTradeIntPx ( (best_nonself_ask_int_price_ - 1), current_tradevarset_.l1ask_trade_size_, kTradeTypeSell, 'A' ) ;
                placed_asks_this_round_ = true;
                last_agg_sell_msecs_ = watch_.msecs_from_midnight();
                if ( dbglogger_.CheckLoggingLevel ( TRADING_INFO ) ) //zero logging
                {
                    DBGLOG_TIME_CLASS_FUNC
                      << "Sending improve S at px " << best_nonself_ask_int_price_ -1
                      << " position " << my_position_
                      << DBGLOG_ENDL_FLUSH ;
                }
            }
        }
    }
    else
    {
        if ( ( dep_market_view_.spread_increments () > 1 ) && (  ! ask_improve_keep_ ) ) 
        # Need to cancel these kind of orders only when the spread > 1
        # In other cases it wont be benificial except wasting 1 message 
        {
            int cancelled_size_ = order_manager_.CancelAsksAboveIntPrice ( best_nonself_ask_int_price_ ) ; 
            if ( cancelled_size_ > 0 )
            {
                if ( dbglogger_.CheckLoggingLevel ( TRADING_INFO  ) )
                {
                    DBGLOG_TIME_CLASS_FUNC << " Cancelling Improve Ask orders Above: " << best_nonself_ask_int_price_
                               << " position: " << my_position_
                               << " tgt_bias: " << targetbias_numbers_ / dep_market_view_.min_price_increment()
                               << " thresh_t: " << current_tradevarset_.l1ask_improve_keep_ / dep_market_view_.min_price_increment()
                               << DBGLOG_ENDL_FLUSH;
                }
            }
         }
    }

    if ( ! placed_asks_this_round_ )
    {
        # get to this location if no aggressive or improve orders placed in this cycle
        if ( top_ask_place_ )
        {
            # only place Ask orders when there is no active unconfirmed order at or above best_nonself_ask_int_price_
            #      and no confirmed order at or above the best price
            if ( ( ( param_set_.place_multiple_orders_ &&
                     ( our_ask_orders_ < param_set_.unit_trade_size_ * num_max_orders_ ) &&
                     ( ( our_ask_orders_  - my_position_ + current_tradevarset_.l1ask_trade_size_ ) < param_set_.max_position_ ) ) ||
                   ( ( order_manager_.SumAskSizeUnconfirmedEqAboveIntPrice ( best_nonself_ask_int_price_ ) == 0 ) &&
             ( order_manager_.SumAskSizeConfirmedEqAboveIntPrice ( best_nonself_ask_int_price_ ) == 0 ) ) ) &&  
         ( stdev_ <= param_set_.low_stdev_lvl_ || ( dep_market_view_.spread_increments() <= param_set_.max_int_spread_to_place_ ) ) ) // Don't place any new orders in inside market if the spread is too wide
            {
                order_manager_.SendTrade ( best_nonself_ask_price_, best_nonself_ask_int_price_, current_tradevarset_.l1ask_trade_size_, kTradeTypeSell, 'B' ) ;
                if ( dbglogger_.CheckLoggingLevel ( TRADING_INFO ) ) //zero logging
                {
                    DBGLOG_TIME_CLASS_FUNC
                      << "SendTrade S of " << current_tradevarset_.l1ask_trade_size_ << " @ " << best_nonself_ask_price_
                      << " tgt_bias: " << -targetbias_numbers_ / dep_market_view_.min_price_increment()
                      << " thresh_t: " << position_tradevarset_map_[  GetPositonToTradeVarsetMapIndex ( effective_ask_position_ ) ].l1ask_place_ / dep_market_view_.min_price_increment()
                      << " Int Px: " << best_nonself_ask_int_price_
                      << " tMktSz: " << best_nonself_ask_size_
                      << " Mkt: " << best_nonself_bid_size_ << " @ " << best_nonself_bid_price_ << " ---- " << best_nonself_ask_price_ << " @ " << best_nonself_ask_size_
                      << DBGLOG_ENDL_FLUSH;
                }
            }
        }
        else
        {
            if ( ! top_ask_keep_ )
            {
                # cancel all orders at best_nonself_ask_price_
                int canceled_size_ = 0;
                if ( param_set_.place_multiple_orders_ ) 
                {
                    order_manager_.CancelAsksEqAboveIntPrice ( best_nonself_ask_int_price_, param_set_.unit_trade_size_ ) ;
                }
                else
                {
                    order_manager_.CancelAsksEqAboveIntPrice ( best_nonself_ask_int_price_ ) ;
                }
                if ( canceled_size_ > 0 )
                {
                    canceled_asks_this_round_ = true;
                    if ( dbglogger_.CheckLoggingLevel ( TRADING_INFO ) ) //zero logging
                    {
                        DBGLOG_TIME
                          << "Canceled S of " << canceled_size_ << " EqAbove " << best_nonself_ask_price_
                          << " tgt_bias: " << -targetbias_numbers_ / dep_market_view_.min_price_increment()
                          << " thresh_t: " << position_tradevarset_map_[  GetPositonToTradeVarsetMapIndex ( effective_ask_position_to_keep_ ) ].l1ask_keep_ / dep_market_view_.min_price_increment()
                          << " tMktSz: " << best_nonself_ask_size_
                          << DBGLOG_ENDL_FLUSH;
                    }
                }
            }
        }
    }

    # zero logging
    if (( dbglogger_.CheckLoggingLevel ( TRADING_INFO ) && ( placed_bids_this_round_ || placed_asks_this_round_ ) ) )
    {
        PrintFullStatus ( );
    }

    # temporarily printing indicators every time
    if ( ( livetrading_ || dbglogger_.CheckLoggingLevel (TRADING_INFO) ) && ( placed_bids_this_round_ || placed_asks_this_round_ || canceled_bids_this_round_ || canceled_asks_this_round_ ) )
    {
        dump_inds = true;
    }
}