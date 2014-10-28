from OrderManager.base_order import BaseOrder

class BaseOrderManager:

    INT_PRICE_RANGE = 50 #2048
    
    def __init__(self, _watch_, _base_trader_, _smv_, _dep_shortcode_, _min_price_increment_):
        self.watch_ = _watch_
        self.base_trader_ = _base_trader_
        self.shortcode_ = _dep_shortcode_
        self.smv_ = _smv_
        self.sum_ask_confirmed_ = [0]*BaseOrderManager.INT_PRICE_RANGE
        self.sum_bid_confirmed_ = [0]*BaseOrderManager.INT_PRICE_RANGE        
        #self.sum_ask_unconfirmed_ = [0]*BaseOrderManager.INT_PRICE_RANGE
        #self.sum_bid_unconfirmed_ = [0]*BaseOrderManager.INT_PRICE_RANGE
        self.initial_adjustment_set_ = False
        self.bid_int_price_adjustment_ = 0
        self.ask_int_price_adjustment_ =  0
        self.order_vec_top_bid_index_  = -1
        self.order_vec_bottom_bid_index_ = -1
        self.confirmed_top_bid_index_ = -1
        self.confirmed_bottom_bid_index_ = -1
        #self.unconfirmed_top_bid_index_ = -1
        #self.unconfirmed_bottom_bid_index_ = -1
        self.order_vec_top_ask_index_ = -1
        self.order_vec_bottom_ask_index_ = -1
        self.confirmed_top_ask_index_ = -1
        self.confirmed_bottom_ask_index_ = -1
        #self.unconfirmed_top_ask_index_ = -1
        #self.unconfirmed_bottom_ask_index_ = -1
        #self.unsequenced_bids_ = []
        #self.unsequenced_asks_ = []
        #self.external_cancel_all_outstanding_orders_ = False
        #self.num_unconfirmed_orders_ = 0
        #self.s_p_position_change_listener_ = []
        #self.position_change_listener_vec_ = []
        #self.s_p_execution_listener_ = []
        #self.execution_listener_vec_ = []
        #self.s_p_order_change_listener_ = []
        #self.order_change_listener_vec_ = []
        #self.s_p_cxl_reject_listener_ = []
        #self.cxl_reject_listener_vec_ = []
        #self.s_p_reject_funds_listener_ = []
        #self.reject_due_to_funds_listener_vec_ = []
        self.client_position_ = 0
        #self.global_position_ = 0
        #self.map_clean_counter_ = 0
        self.sum_bid_sizes_ = 0
        self.sum_ask_sizes_ = 0
        self.num_self_trades_ = 0
        #self.trade_volume_ = 0
        #self.last_maps_cleaned_msecs_ = 0
        #self.last_top_replay_msecs_ = 0
        #self.queue_sizes_needed_ = False
        #self.best_bid_int_price_ = 0
        #self.best_ask_int_price_ = 0
        #self.supporting_order_filled_= 0
        #self.best_level_order_filled_ = 0
        #self.aggressive_order_filled_ = 0
        #self.improve_order_filled_ = 0
        self.total_size_placed_ = 0
        self.send_order_count_ = 0
        self.cancel_order_count_ = 0
        self.base_pnl_ = None
        self.trade_volume_ = 0
        #self.security_id_to_last_position_( sec_name_indexer_.NumSecurityId ( ) , kInvalidPosition ) , security_position_ ( 0 ) ,// To maintain positions for all contracts of this security.
        #self.p_ticks_to_keep_bid_int_price_ = None
        #self.p_ticks_to_keep_ask_int_price_ = None
        #self.throttle_manager_ = None
        self.client_assigned_order_sequence_ = 0
        self.bid_order_vec_ = []
        self.ask_order_vec_ = []
        self.position_update_listeners_ = []
        for i in range(0, BaseOrderManager.INT_PRICE_RANGE):
            self.bid_order_vec_.append([])
            self.ask_order_vec_.append([])
        
        
    def AddPositionUpdateListener(self, _listener_):
        if (not _listener_ in self.position_update_listeners_):
            self.position_update_listeners_.append(_listener_)
        
    def PrintStatistics(self):
        print('Total Size Placed:\t'+str(self.total_size_placed_))
        print('Send Order Count:\t'+str(self.send_order_count_))
        print('Cancel Order Count:\t'+str(self.cancel_order_count_))
        print('Traded Volume:\t\t'+str(self.trade_volume_))
        print('Client Position:\t'+str(self.client_position_))
    
    def Dump(self):
        for order_vec_ in self.bid_order_vec_:
            if (not order_vec_):
                continue
            for order_ in order_vec_:
                order_.dump()
        for order_vec_ in self.ask_order_vec_:
            if (not order_vec_):
                continue
            for order_ in order_vec_:
                order_.dump()
        print self.sum_bid_confirmed_,
        for sum1 in self.sum_bid_confirmed_:
            if (sum1 != 0):
                print 'Sum:='+str(sum1),
        for sum1 in self.sum_ask_confirmed_:
            if (sum1 != 0):
                print 'Sum:='+str(sum1),
#         print '-----------------------------------'
#         print 'shortcode_:\t\t\t'+self.shortcode_
# 
#         print 'sum_bid_confirmed_:\t\t'+str(self.sum_bid_confirmed_)
#         print 'sum_ask_confirmed_:\t\t'+str(self.sum_ask_confirmed_)
#         
#         #print 'sum_bid_unconfirmed_:\t\t'+str(self.sum_bid_unconfirmed_)
#         #print 'sum_ask_unconfirmed_:\t\t'+str(self.sum_ask_unconfirmed_)
#         
#         print 'bid_order_vec_:\t\t\t'+str(self.bid_order_vec_)
#         print 'ask_order_vec_:\t\t\t'+str(self.ask_order_vec_)
#         
#         print 'initial_adjustment_set_:\t'+str(self.initial_adjustment_set_)
#         print 'bid_int_price_adjustment:\t'+str(self.bid_int_price_adjustment_)
#         print 'ask_int_price_adjustment:\t'+str(self.ask_int_price_adjustment_)
# 
#         print 'order_vec_top_bid_index_:\t'+str(self.order_vec_top_bid_index_)
#         print 'order_vec_bottom_bid_index_:\t'+str(self.order_vec_bottom_bid_index_)
#         print 'confirmed_top_bid_index_:\t'+str(self.confirmed_top_bid_index_)
#         print 'confirmed_bottom_bid_index_:\t'+str(self.confirmed_bottom_bid_index_)
#         #print 'unconfirmed_top_bid_index_:\t'+str(self.unconfirmed_top_bid_index_)
#         #print 'unconfirmed_bottom_bid_index_:\t'+str(self.unconfirmed_bottom_bid_index_)
#         
#         print 'order_vec_top_ask_index_:\t'+str(self.order_vec_top_ask_index_)
#         print 'order_vec_bottom_ask_index_:\t'+str(self.order_vec_bottom_ask_index_)
#         print 'confirmed_top_ask_index_:\t'+str(self.confirmed_top_ask_index_)
#         print 'confirmed_bottom_ask_index_:\t'+str(self.confirmed_bottom_ask_index_)
#         #print 'unconfirmed_top_ask_index_:\t'+str(self.unconfirmed_top_ask_index_)
#         #print 'unconfirmed_bottom_ask_index_:\t'+str(self.unconfirmed_bottom_ask_index_)        
# 
#         #print 'unsequenced_bids_:\t\t', self.unsequenced_bids_
#         #print 'unsequenced_asks_:\t\t', self.unsequenced_asks_
#         #print 'num_unconfimed_orders_:\t\t'+str(self.num_unconfirmed_orders_)
#         print 'client_position_:\t\t'+str(self.client_position_)
#         #print 'global_position_:\t\t'+str(self.global_position_)
#         print 'sum_bid_sizes_:\t\t\t'+str(self.sum_bid_sizes_)
#         print 'sum_ask_sizes_:\t\t\t'+str(self.sum_ask_sizes_)
#         #print 'best_bid_int_price_:\t\t'+str(self.best_bid_int_price_)
#         #print 'best_ask_int_price_:\t\t'+str(self.best_ask_int_price_)
#         print 'total_size_placed_:\t\t'+str(self.total_size_placed_)
#         print 'send_order_count_:\t\t'+str(self.send_order_count_)
#         print 'cancel_order_count_:\t\t'+str(self.cancel_order_count_)
#         print 'caos_:\t\t\t\t'+str(self.client_assigned_order_sequence_)
#         print '-----------------------------------'
        
    def OrderExecuted(self, t_server_assigned_client_id_, _client_assigned_order_sequence_, t_server_assigned_order_sequence_, 
                      _security_id_, _price_, t_buysell_, _size_remaining_, _size_executed_, t_client_position_, 
                      t_global_position_, r_int_price_):
        self.global_position_ = t_global_position_
        if (t_server_assigned_client_id_ == t_server_assigned_client_id_): #hack
            #self.num_self_trades_ += 1
            if (t_buysell_ == 'B'):
                bid_index_ = self.GetBidIndex(r_int_price_)
                # search in sequenced orders at the price sent by ORS
                # fetch order in intpx_2_bid_order_vec_[r_int_price_]
                this_base_order_vec_ = self.bid_order_vec_[bid_index_]
                if (not this_base_order_vec_):
                    print('Not possible')
                for order_ in this_base_order_vec_[:]:
                    if (order_.client_assigned_order_sequence() != t_server_assigned_order_sequence_): ##
                        continue
                    #if (order_.server_assigned_order_sequence() == t_server_assigned_order_sequence_):
                    # Found the order
                    if (order_.order_status() == 'Conf'):
                        self.sum_bid_confirmed_[bid_index_] = max(0, self.sum_bid_confirmed_[bid_index_] + _size_remaining_ - order_.size_remaining())
                        self.AdjustTopBottomConfirmedBidIndexes (bid_index_)
                        if (_size_remaining_ > 0):
                            # order is stil live so set size appropriately
                            order_.ConfirmNewSize(_size_remaining_) # set both size_requested_ and size_remaining_ to this value

                    # Update active bid
                    self.sum_bid_sizes_ -= _size_executed_
                    if (_size_remaining_ <= 0):
                        this_base_order_vec_.remove(order_) # remove order from vec
                        self.AdjustTopBottomOrderVecBidIndexes(bid_index_)
                    break
            else:
                ask_index_ = self.GetAskIndex(r_int_price_)
                # search in sequenced orders at the price sent by ORS
                # fetch order in intpx_2_ask_order_vec_[r_int_price_]
                this_base_order_vec_ = self.ask_order_vec_[ask_index_]
                if (not this_base_order_vec_):
                    print('Not possible')
                for order_ in this_base_order_vec_[:]:
                    if (order_.client_assigned_order_sequence() == t_server_assigned_order_sequence_):
                    #if (order_.server_assigned_order_sequence() == t_server_assigned_order_sequence_):
                        # Found the order
                        if (order_.order_status() == 'Conf'):
                            self.sum_ask_confirmed_[ask_index_] = max(0, self.sum_ask_confirmed_[ask_index_] + _size_remaining_ - order_.size_remaining())
                            self.AdjustTopBottomConfirmedAskIndexes(ask_index_)
                            if (_size_remaining_ > 0):
                                # order is stil live so set size appropriately
                                order_.ConfirmNewSize(_size_remaining_) # set both size_requested_ and size_remaining_ to this value
                        
                        # Update active ask
                        self.sum_ask_sizes_ -= _size_executed_
                        if (_size_remaining_ <= 0):
                            this_base_order_vec_.remove(order_) # remove order from vec
                            self.AdjustTopBottomOrderVecAskIndexes(ask_index_)
                        break
            self.AdjustPosition(t_client_position_, _price_, r_int_price_) # instead of GetMidPrice() use _price_ sent
            
            
    def OrderCanceled(self, t_server_assigned_client_id_, _client_assigned_order_sequence_, t_server_assigned_order_sequence_, 
                      _security_id_, _price_, t_buysell_, _size_remaining_, _size_executed_, t_client_position_, 
                      t_global_position_, r_int_price_):
        self.global_position_ = t_global_position_
        if (t_server_assigned_client_id_ == t_server_assigned_client_id_): #hack
            #print 'hello'
            if (t_buysell_ == 'B'):
                bid_index_ = self.GetBidIndex(r_int_price_)
                _this_base_order_vec_ = self.bid_order_vec_[bid_index_]
                if (_this_base_order_vec_):
                    for order_ in _this_base_order_vec_[:]:
                        if (not order_.server_assigned_order_sequence() == t_server_assigned_order_sequence_):
                            continue
                        if (order_.order_status() == 'Conf'):
                            self.sum_bid_confirmed_[bid_index_] = max(0, self.sum_bid_confirmed_[bid_index_] - order_.size_remaining())
                            self.AdjustTopBottomConfirmedBidIndexes(bid_index_)
                            self.sum_bid_sizes_ -= order_.size_remaining()
                        _this_base_order_vec_.remove(order_) # remove order from vec
                        self.AdjustTopBottomOrderVecBidIndexes(bid_index_)
            else:
                ask_index_ = self.GetAskIndex(r_int_price_)
                _this_base_order_vec_ = self.ask_order_vec_[ask_index_]
                if (_this_base_order_vec_):
                    for order_ in _this_base_order_vec_[:]:
                        if (not order_.server_assigned_order_sequence() == t_server_assigned_order_sequence_):
                            continue
                        if (order_.order_status() == 'Conf'):
                            self.sum_ask_confirmed_[ask_index_] = max(0, self.sum_ask_confirmed_[ask_index_] - order_.size_remaining())
                            self.AdjustTopBottomConfirmedAskIndexes(ask_index_)
                            self.sum_ask_sizes_ -= order_.size_remaining()
                        _this_base_order_vec_.remove(order_) # remove order from vec
                        self.AdjustTopBottomOrderVecAskIndexes(ask_index_)
            if (self.client_position_ != t_client_position_):
                self.AdjustPosition(t_client_position_, self.smv_.GetMidPrice(), self.smv_.GetMidIntPrice())
            
    def AdjustPosition(self, t_client_position_, _trade_price_, r_int_price_):
        # this can be called any number of times ... ti will only do sth if client_position_ != t_client_position_
        if (self.client_position_ != t_client_position_):
            for listener_ in self.position_update_listeners_:
                listener_.OnPositionUpdate(t_client_position_)
            if (t_client_position_ > self.client_position_):
                _implied_buysell_ = 'B'
            else:
                _implied_buysell_ = 'S'
            position_diff_ = abs(t_client_position_ - self.client_position_)
            self.trade_volume_ += position_diff_
            # updating position here since this gives control to strategy
            self.client_position_ = t_client_position_
            # NotifyExecutionListeners
            self.base_pnl_.OnExec(t_client_position_, position_diff_, _implied_buysell_, _trade_price_, r_int_price_)
    
    def GetBidIndex(self, _int_price_):
        if (not self.initial_adjustment_set_):
            self.SetInitialIntPriceAdjustment(_int_price_)
        return _int_price_ - self.bid_int_price_adjustment_
    
    def GetAskIndex(self, _int_price_):
        if (not self.initial_adjustment_set_):
            self.SetInitialIntPriceAdjustment(_int_price_)
        return (self.INT_PRICE_RANGE - (_int_price_ - self.ask_int_price_adjustment_))
    
    def SetInitialIntPriceAdjustment(self, _int_price_):
        self.bid_int_price_adjustment_ = _int_price_ - self.INT_PRICE_RANGE / 2
        self.ask_int_price_adjustment_ = _int_price_ - self.INT_PRICE_RANGE / 2
        self.initial_adjustment_set_ = True
        '''Assumption: No re-adjustment is needed'''
    
    def SetBasePNL(self, _base_pnl_):
        self.base_pnl_ = _base_pnl_
    
    def CancelAllOrders(self):
        self.CancelAllBidOrders()
        self.CancelAllAskOrders()
        
    def CancelAllBidOrders(self):
        if (self.order_vec_top_bid_index_ == -1):
            return
        t_index_ = self.order_vec_top_bid_index_
        while (t_index_ >= self.order_vec_bottom_bid_index_):
            for t_order_ in self.bid_order_vec_[t_index_]:
                self.Cancel(t_order_)
            t_index_ -= 1
    
    def CancelAllAskOrders(self):
        if (self.order_vec_top_ask_index_ == -1):
            return
        t_index_ = self.order_vec_top_ask_index_
        while (t_index_ >= self.order_vec_bottom_ask_index_):
            for t_order_ in self.ask_order_vec_[t_index_]:
                self.Cancel(t_order_)
            t_index_ -= 1

    def CancelBidsEqAboveIntPrice(self, _intpx_):
        t_retval_ = 0
        t_retval_ += self.CancelBidsAtIntPrice(_intpx_)
        t_retval_ += self.CancelBidsAboveIntPrice(_intpx_)
        return t_retval_
    
    def CancelBidsEqBelowIntPrice(self, _intpx_):
        t_retval_ = 0
        t_retval_ += self.CancelBidsAtIntPrice(_intpx_)
        t_retval_ += self.CancelBidsBelowIntPrice(_intpx_)
        return t_retval_
        
    def CancelBidsAtIntPrice(self, _intpx_):
        if (self.order_vec_top_bid_index_ == -1):
            return 0
        t_index_ = self.GetBidIndex(_intpx_)
        return self.CancelOrdersInVec(self.bid_order_vec_[t_index_])
    
    def CancelBidsAboveIntPrice(self, _intpx_):
        if (self.order_vec_top_bid_index_ == -1):
            return 0
        t_retval_ = 0
        t_bid_index_ = self.GetBidIndex(_intpx_)
        t_index_ = self.order_vec_top_bid_index_
        while (t_index_ > max(t_bid_index_, self.order_vec_bottom_bid_index_ - 1)):
            t_retval_ += self.CancelOrdersInVec(self.bid_order_vec_[t_index_])
            t_index_ -= 1
        return t_retval_
        
    def CancelBidsBelowIntPrice(self, _intpx_):
        if (self.order_vec_top_bid_index_ == -1):
            return 0
        t_retval_ = 0
        t_bid_index_ = self.GetBidIndex(_intpx_)
        t_index_ = self.order_vec_bottom_bid_index_
        while (t_index_ < min(t_bid_index_, self.order_vec_bottom_bid_index_ + 1)):
            t_retval_ += self.CancelOrdersInVec(self.bid_order_vec_[t_index_])
            t_index_ += 1
        return t_retval_
    
    def CancelBidsFromFar(self, _requested_size_):
        if (self.order_vec_top_bid_index_ == -1):
            return 0
        t_retval_ = 0
        t_index_ = self.order_vec_bottom_bid_index_
        while (t_index_ <= self.order_vec_top_bid_index_):
            t_retval_ += self.CancelOrdersInVec(self.bid_order_vec_[t_index_])
            if (t_retval_ >= _requested_size_):
                break
            t_index_ += 1
        return t_retval_
    
    def CancelAsksEqAboveIntPrice(self, _intpx_):
        t_retval_ = 0
        t_retval_ += self.CancelAsksAtIntPrice(_intpx_)
        t_retval_ += self.CancelAsksAboveIntPrice(_intpx_)
        return t_retval_
    
    def CancelAsksEqBelowIntPrice(self, _intpx_):
        t_retval_ = 0
        t_retval_ += self.CancelAsksAtIntPrice(_intpx_)
        t_retval_ += self.CancelAsksBelowIntPrice(_intpx_)
        return t_retval_
        
    def CancelAsksAtIntPrice(self, _intpx_):
        if (self.order_vec_top_ask_index_ == -1):
            return 0
        t_index_ = self.GetAskIndex(_intpx_)
        return self.CancelOrdersInVec(self.ask_order_vec_[t_index_])
    
    def CancelAsksAboveIntPrice(self, _intpx_):
        if (self.order_vec_top_ask_index_ == -1):
            return 0
        t_retval_ = 0
        t_ask_index_ = self.GetAskIndex(_intpx_)
        t_index_ = self.order_vec_top_ask_index_
        while (t_index_ > max(t_ask_index_, self.order_vec_bottom_ask_index_ - 1)):
            t_retval_ += self.CancelOrdersInVec(self.ask_order_vec_[t_index_])
            t_index_ -= 1
        return t_retval_
        
    def CancelAsksBelowIntPrice(self, _intpx_):
        if (self.order_vec_top_ask_index_ == -1):
            return 0
        t_retval_ = 0
        t_ask_index_ = self.GetAskIndex(_intpx_)
        t_index_ = self.order_vec_bottom_ask_index_
        while (t_index_ < min(t_ask_index_, self.order_vec_bottom_ask_index_ + 1)):
            t_retval_ += self.CancelOrdersInVec(self.ask_order_vec_[t_index_])
            t_index_ += 1
        return t_retval_
    
    def CancelAsksFromFar(self, _requested_size_):
        if (self.order_vec_top_ask_index_ == -1):
            return 0
        t_retval_ = 0
        t_index_ = self.order_vec_bottom_ask_index_
        while (t_index_ <= self.order_vec_top_ask_index_):
            t_retval_ += self.CancelOrdersInVec(self.ask_order_vec_[t_index_])
            if (t_retval_ >= _requested_size_):
                break
            t_index_ += 1
        return t_retval_
        
    def CancelOrdersInVec(self, _order_vec_):
        t_retval_ = 0
        for t_order_ in _order_vec_:
            if (self.Cancel(t_order_)):
                t_retval_ += t_order_.size_remaining()
        return t_retval_

    '''Aggregator functions'''
    
    '''Bid version'''    '''
    def SumBidSizeUnconfirmedEqAboveIntPrice(self, _intpx_):
        if (self.unconfirmed_top_bid_index_ == -1):
            return 0
        t_bid_index_ = self.GetBidIndex(_intpx_)
        t_index_ = self.unconfirmed_top_bid_index_
        t_retval_ = 0
        while (t_index_ >= max(t_bid_index_, self.unconfirmed_bottom_bid_index_)):
            t_retval_ += self.sum_bid_unconfirmed_[t_index_]
            t_index_ -= 1
        return t_retval_'''
    
    def SumBidSizeConfirmedEqAboveIntPrice(self, _intpx_):
        #print self.confirmed_top_bid_index_,
        #print self.confirmed_bottom_bid_index_,
        if (self.confirmed_top_bid_index_ == -1):
            return 0
        t_bid_index_ = self.GetBidIndex(_intpx_)
        t_index_ = self.confirmed_top_bid_index_
        t_retval_ = 0
        while (t_index_ >= max(t_bid_index_, self.confirmed_bottom_bid_index_)):
            t_retval_ += self.sum_bid_confirmed_[t_index_]
            t_index_ -= 1
        return t_retval_
    
    def SumBidSizeConfirmedAboveIntPrice(self, _intpx_):
        if (self.confirmed_top_bid_index_ == -1):
            return 0
        t_bid_index_ = self.GetBidIndex(_intpx_)
        t_index_ = self.confirmed_top_bid_index_
        t_retval_ = 0
        while (t_index_ > max(t_bid_index_, self.confirmed_bottom_bid_index_ - 1)):
            t_retval_ += self.sum_bid_confirmed_[t_index_]
            t_index_ -= 1
        return t_retval_
    
    def SumBidSizes(self):
        t_retval_ = 0
        '''
        if (self.unconfirmed_top_bid_index_ != -1):
            t_index_ = self.unconfirmed_top_bid_index_
            while (t_index_ >= self.unconfirmed_bottom_bid_index_):
                t_retval_ += self.sum_bid_unconfirmed_[t_index_]
                t_index_ -= 1'''
        if (self.confirmed_top_bid_index_ != -1):
            t_index_ = self.confirmed_top_bid_index_
            while (t_index_ >= self.confirmed_bottom_bid_index_):
                t_retval_ += self.sum_bid_confirmed_[t_index_]
                t_index_ -= 1

    '''Ask version'''
    '''
    def SumAskSizeUnconfirmedEqAboveIntPrice(self, _intpx_):
        if (self.unconfirmed_top_ask_index_ == -1):
            return 0
        t_ask_index_ = self.GetAskIndex(_intpx_)
        t_index_ = self.unconfirmed_top_ask_index_
        t_retval_ = 0
        while (t_index_ >= max(t_ask_index_, self.unconfirmed_bottom_ask_index_)):
            t_retval_ += self.sum_ask_unconfirmed_[t_index_]
            t_index_ -= 1
        return t_retval_'''
    
    def SumAskSizeConfirmedEqAboveIntPrice(self, _intpx_):
        if (self.confirmed_top_ask_index_ == -1):
            return 0
        t_ask_index_ = self.GetAskIndex(_intpx_)
        t_index_ = self.confirmed_top_ask_index_
        t_retval_ = 0
        while (t_index_ >= max(t_ask_index_, self.confirmed_bottom_ask_index_)):
            t_retval_ += self.sum_ask_confirmed_[t_index_]
            t_index_ -= 1
        return t_retval_
    
    def SumAskSizeConfirmedAboveIntPrice(self, _intpx_):
        if (self.confirmed_top_ask_index_ == -1):
            return 0
        t_ask_index_ = self.GetAskIndex(_intpx_)
        t_index_ = self.confirmed_top_ask_index_
        t_retval_ = 0
        while (t_index_ > max(t_ask_index_, self.confirmed_bottom_ask_index_ - 1)):
            t_retval_ += self.sum_ask_confirmed_[t_index_]
            t_index_ -= 1
        return t_retval_
    
    def SumAskSizes(self):
        t_retval_ = 0
        '''
        if (self.unconfirmed_top_ask_index_ != -1):
            t_index_ = self.unconfirmed_top_ask_index_
            while (t_index_ >= self.unconfirmed_bottom_ask_index_):
                t_retval_ += self.sum_ask_unconfirmed_[t_index_]
                t_index_ -= 1'''
        if (self.confirmed_top_ask_index_ != -1):
            t_index_ = self.confirmed_top_ask_index_
            while (t_index_ >= self.confirmed_bottom_ask_index_):
                t_retval_ += self.sum_ask_confirmed_[t_index_]
                t_index_ -= 1

    def Cancel(self, _order_):
        if (_order_.CanBeCanceled()):
            _order_.canceled_ = True
            self.base_trader_.Cancel(_order_)
            self.cancel_order_count_ += 1
            return True
        else:
            return False
                
    def SendTrade(self, _price_, _int_price_, _size_requested_, _buysell_):
        #self.Dump()

        #print('SendTrade Called')
        #print _price_, _int_price_, _size_requested_, _buysell_
        #exit()
        print('Send'),
        if (_size_requested_ <= 0):
            print 'SendTrade: _size_requested_ <= 0'
            return
        order_ = BaseOrder()
        order_.security_name_ = self.shortcode_
        order_.buysell_ = _buysell_
        order_.price_ = _price_
        order_.int_price_ = _int_price_
        order_.size_requested_ = _size_requested_
        order_.size_remaining_ = _size_requested_
        order_.order_status_ = 'Conf' # In original order_manager_, this would have been 'None' -> 'Seqd' -> 'Conf', 
        #we assume that once an order is sent to the exchange, it will always get confirmed, also we assume delay to be zero!!
        order_.client_assigned_order_sequence_ = self.client_assigned_order_sequence_
        self.client_assigned_order_sequence_ += 1
        # since we will have only one client, so caos and saos will be same (so we don't need the sequenced thingy!)
        
        if (_buysell_ == 'B'): # Buy
            t_bid_index_ = self.GetBidIndex(_int_price_)
            #self.sum_bid_unconfirmed_[t_bid_index_] += _size_requested_
            #self.AdjustTopBottomUnconfirmedBidIndexes(t_bid_index_)
            #self.unsequenced_bids_.append(order_)
            #self.num_unconfirmed_orders_ += 1
            self.bid_order_vec_[t_bid_index_].append(order_)
            order_.server_assigned_order_sequence_ = order_.client_assigned_order_sequence_ # hack
            self.AdjustTopBottomOrderVecBidIndexes(t_bid_index_)
            self.sum_bid_confirmed_[t_bid_index_] += order_.size_requested_
            self.AdjustTopBottomConfirmedBidIndexes(t_bid_index_)
            self.sum_bid_sizes_ += _size_requested_
        else:
            t_ask_index_ = self.GetAskIndex(_int_price_)
#             self.sum_ask_unconfirmed_[t_ask_index_] += _size_requested_
#             self.AdjustTopBottomUnconfirmedAskIndexes(t_ask_index_)
#             self.unsequenced_bids_.append(order_)
#             self.num_unconfirmed_orders_ += 1
            self.ask_order_vec_[t_ask_index_].append(order_)
            order_.server_assigned_order_sequence_ = order_.client_assigned_order_sequence_ # hack
            self.AdjustTopBottomOrderVecAskIndexes(t_ask_index_)
            self.sum_ask_confirmed_[t_ask_index_] += order_.size_requested_
            self.AdjustTopBottomConfirmedAskIndexes(t_ask_index_)
            self.sum_ask_sizes_ += _size_requested_
        
        order_.dump()
        #self.Dump()

        self.base_trader_.SendTrade(order_)
        
        self.total_size_placed_ += _size_requested_
        self.send_order_count_ += 1
        #self.Dump()
        
    '''Adjust Function''' 
    '''
    def AdjustTopBottomUnconfirmedBidIndexes(self, _bid_index_):
        if (self.sum_bid_unconfirmed_[_bid_index_] == 0):
            if (_bid_index_ == self.unconfirmed_top_bid_index_ and _bid_index_ == self.unconfirmed_bottom_bid_index_):
                self.unconfirmed_top_bid_index_ = -1
                self.unconfirmed_bottom_bid_index_ = -1
            elif (_bid_index_ == self.unconfirmed_top_bid_index_):
                while (self.sum_bid_unconfirmed[self.unconfirmed_top_bid_index_] == 0):
                    self.unconfirmed_top_bid_index_ -= 1
            elif (_bid_index_ == self.unconfirmed_bottom_bid_index_):
                while (self.sum_bid_unconfirmed[self.unconfirmed_bottom_bid_index_] == 0):
                    self.unconfirmed_bottom_bid_index_ += 1
            else:
                pass
        else:
            if (self.unconfirmed_top_bid_index_ == -1):
                assert self.unconfirmed_bottom_bid_index_ == -1
                self.unconfirmed_bottom_bid_index_ = _bid_index_
                self.unconfirmed_top_bid_index_ = _bid_index_
            elif (_bid_index_ > self.unconfirmed_top_bid_index_):
                self.unconfirmed_top_bid_index_ = _bid_index_
            elif (_bid_index_ < self.unconfirmed_bottom_bid_index_):
                self.unconfirmed_bottom_bid_index_ = _bid_index_
            else:
                pass
        assert self.unconfirmed_bottom_bid_index_ <= self.unconfirmed_top_bid_index_'''
        
    def AdjustTopBottomConfirmedBidIndexes(self, _bid_index_):
        if (self.sum_bid_confirmed_[_bid_index_] == 0):
            if (_bid_index_ == self.confirmed_top_bid_index_ and _bid_index_ == self.confirmed_bottom_bid_index_):
                self.confirmed_top_bid_index_ = -1
                self.confirmed_bottom_bid_index_ = -1
            elif (_bid_index_ == self.confirmed_top_bid_index_):
                while (self.sum_bid_confirmed_[self.confirmed_top_bid_index_] == 0):
                    self.confirmed_top_bid_index_ -= 1
            elif (_bid_index_ == self.confirmed_bottom_bid_index_):
                while (self.sum_bid_confirmed_[self.confirmed_bottom_bid_index_] == 0):
                    self.confirmed_bottom_bid_index_ += 1
            else:
                pass
        else:
            if (self.confirmed_top_bid_index_ == -1):
                assert self.confirmed_bottom_bid_index_ == -1
                self.confirmed_bottom_bid_index_ = _bid_index_
                self.confirmed_top_bid_index_ = _bid_index_
            elif (_bid_index_ > self.confirmed_top_bid_index_):
                self.confirmed_top_bid_index_ = _bid_index_
            elif (_bid_index_ < self.confirmed_bottom_bid_index_):
                self.confirmed_bottom_bid_index_ = _bid_index_
            else:
                pass
        assert self.confirmed_bottom_bid_index_ <= self.confirmed_top_bid_index_
    '''
    def AdjustTopBottomUnconfirmedAskIndexes(self, _ask_index_):
        if (self.sum_ask_unconfirmed_[_ask_index_] == 0):
            if (_ask_index_ == self.unconfirmed_top_ask_index_ and _ask_index_ == self.unconfirmed_bottom_ask_index_):
                self.unconfirmed_top_ask_index_ = -1
                self.unconfirmed_bottom_ask_index_ = -1
            elif (_ask_index_ == self.unconfirmed_top_ask_index_):
                while (self.sum_ask_unconfirmed[self.unconfirmed_top_ask_index_] == 0):
                    self.unconfirmed_top_ask_index_ -= 1
            elif (_ask_index_ == self.unconfirmed_bottom_ask_index_):
                while (self.sum_ask_unconfirmed[self.unconfirmed_bottom_ask_index_] == 0):
                    self.unconfirmed_bottom_ask_index_ += 1
            else:
                pass
        else:
            if (self.unconfirmed_top_ask_index_ == -1):
                assert self.unconfirmed_bottom_ask_index_ == -1
                self.unconfirmed_bottom_ask_index_ = _ask_index_
                self.unconfirmed_top_ask_index_ = _ask_index_
            elif (_ask_index_ > self.unconfirmed_top_ask_index_):
                self.unconfirmed_top_ask_index_ = _ask_index_
            elif (_ask_index_ < self.unconfirmed_bottom_ask_index_):
                self.unconfirmed_bottom_ask_index_ = _ask_index_
            else:
                pass
        assert self.unconfirmed_bottom_ask_index_ <= self.unconfirmed_top_ask_index_'''
        
    def AdjustTopBottomConfirmedAskIndexes(self, _ask_index_):
        if (self.sum_ask_confirmed_[_ask_index_] == 0):
            if (_ask_index_ == self.confirmed_top_ask_index_ and _ask_index_ == self.confirmed_bottom_ask_index_):
                self.confirmed_top_ask_index_ = -1
                self.confirmed_bottom_ask_index_ = -1
            elif (_ask_index_ == self.confirmed_top_ask_index_):
                while (self.sum_ask_confirmed_[self.confirmed_top_ask_index_] == 0):
                    self.confirmed_top_ask_index_ -= 1
            elif (_ask_index_ == self.confirmed_bottom_ask_index_):
                while (self.sum_ask_confirmed_[self.confirmed_bottom_ask_index_] == 0):
                    self.confirmed_bottom_ask_index_ += 1
            else:
                pass
        else:
            if (self.confirmed_top_ask_index_ == -1):
                assert self.confirmed_bottom_ask_index_ == -1
                self.confirmed_bottom_ask_index_ = _ask_index_
                self.confirmed_top_ask_index_ = _ask_index_
            elif (_ask_index_ > self.confirmed_top_ask_index_):
                self.confirmed_top_ask_index_ = _ask_index_
            elif (_ask_index_ < self.confirmed_bottom_ask_index_):
                self.confirmed_bottom_ask_index_ = _ask_index_
            else:
                pass
        assert self.confirmed_bottom_ask_index_ <= self.confirmed_top_ask_index_
        
    def AdjustTopBottomOrderVecAskIndexes(self, _ask_index_):
        if (not self.ask_order_vec_[_ask_index_]):
            if (_ask_index_ == self.order_vec_top_ask_index_ and _ask_index_ == self.order_vec_bottom_ask_index_):
                self.order_vec_top_ask_index_ = -1
                self.order_vec_bottom_ask_index_ = -1
            elif (_ask_index_ == self.order_vec_top_ask_index_):
                while (not self.ask_order_vec_[self.order_vec_top_ask_index_]):
                    self.order_vec_top_ask_index_ -= 1
            elif (_ask_index_ == self.order_vec_bottom_ask_index_):
                while (not self.ask_order_vec_[self.order_vec_bottom_ask_index_]):
                    self.order_vec_bottom_ask_index_ += 1
            else:
                pass
        else:
            if (self.order_vec_top_ask_index_ == -1):
                assert self.order_vec_bottom_ask_index_ == -1
                self.order_vec_top_ask_index_ = _ask_index_
                self.order_vec_bottom_ask_index_ = _ask_index_
            elif (_ask_index_ > self.order_vec_top_ask_index_):
                self.order_vec_top_ask_index_ = _ask_index_
            elif (_ask_index_ < self.order_vec_bottom_ask_index_):
                self.order_vec_bottom_ask_index_ = _ask_index_
            else:
                pass
        assert self.order_vec_bottom_ask_index_ <= self.order_vec_top_ask_index_
        
    def AdjustTopBottomOrderVecBidIndexes(self, _bid_index_):
        if (not self.bid_order_vec_[_bid_index_]):
            if (_bid_index_ == self.order_vec_top_bid_index_ and _bid_index_ == self.order_vec_bottom_bid_index_):
                self.order_vec_top_bid_index_ = -1
                self.order_vec_bottom_bid_index_ = -1
            elif (_bid_index_ == self.order_vec_top_bid_index_):
                while (not self.bid_order_vec_[self.order_vec_top_bid_index_]):
                    self.order_vec_top_bid_index_ -= 1
            elif (_bid_index_ == self.order_vec_bottom_bid_index_):
                while (not self.bid_order_vec_[self.order_vec_bottom_bid_index_]):
                    self.order_vec_bottom_bid_index_ += 1
            else:
                pass
        else:
            if (self.order_vec_top_bid_index_ == -1):
                assert self.order_vec_bottom_bid_index_ == -1
                self.order_vec_top_bid_index_ = _bid_index_
                self.order_vec_bottom_bid_index_ = _bid_index_
            elif (_bid_index_ > self.order_vec_top_bid_index_):
                self.order_vec_top_bid_index_ = _bid_index_
            elif (_bid_index_ < self.order_vec_bottom_bid_index_):
                self.order_vec_bottom_bid_index_ = _bid_index_
            else:
                pass
        assert self.order_vec_bottom_bid_index_ <= self.order_vec_top_bid_index_