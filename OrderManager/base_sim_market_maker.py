from OrderManager.base_order import BaseOrder
from MarketAdapter.security_market_view import SecurityMarketViewChangeListener
from ExternalData.external_time_listener import TimePeriodListener        

class BaseSimMarketMaker(SecurityMarketViewChangeListener, TimePeriodListener):
    
    shcToSMMmap = dict()

    '''constructor'''
    def __init__(self, _watch_, _smv_):
        #we must have masked_from_market_data_bids_map_ otherwise even a partial match would fill
        #we 
        #self.global_position_ = 0
        self.client_position_map_ = []
        #self.global_position_to_send_map_ = []
        #self.masked_asks_ = False
        #self.masked_bids_ = False
        #self.masked_from_market_data_bids_map_ = []
        #self.masked_from_market_data_asks_map_ = []
        self.watch_ = _watch_
        #self.all_requests_ = []
        #self.pending_requests_ = []
        #self.all_requests_lock_ = False
        
        self.intpx_to_ask_order_vec_ = {}
        self.intpx_to_bid_order_vec_ = {}
        
        self.dep_market_view_ = _smv_
        #self.bestbid_int_price_ = 0
        #self.bestask_int_price_ = 0 
        #self.bestbid_size_ = 0
        #self.bestask_size_ = 0
        #self.last_bid_size_change_msecs_ = 0
        #self.last_ask_size_change_msecs_ = 0
        #self.ask_side_priority_order_exists_ = False
        #self.ask_side_priority_order_size_ = 0
        #self.bid_side_priority_order_exists_ = False
        #self.bid_side_priority_order_size_ = 0
        #self.dep_market_view_.SubscribePriceType(self, 'MktSizeWPrice')
        self.watch_.SubscribeBigTimePeriod(self) # may make small Time period also in watch
        
        self.server_assigned_order_sequence_ = 0
        #self.saos_to_seqd_time_ = [] # server_assigned_order_sequence
        
        #self.order_rejection_listener_vec_ = []
        #self.order_sequenced_listener_vec_ = []
        self.order_executed_listener_vec_ = []
        self.order_canceled_listener_vec_ = []

        #self.saci_to_executed_size_ = []
        
        self.count_ = 0
        
    def dump(self):
        for price_ in self.intpx_to_bid_order_vec_.keys():
            order_vec_ = self.intpx_to_bid_order_vec_[price_]
            if (not order_vec_):
                continue
            for order_ in order_vec_:
                order_.dump()
        for price_ in self.intpx_to_ask_order_vec_.keys():
            order_vec_ = self.intpx_to_ask_order_vec_[price_]
            if (not order_vec_):
                continue
            for order_ in order_vec_:
                order_.dump()
    
    def AddOrderExecutedListener(self, _listener_):
        if (_listener_ not in self.order_executed_listener_vec_):
            self.order_executed_listener_vec_.append(_listener_)
            
    def AddOrderCanceledListener(self, _listener_):
        if (_listener_ not in self.order_canceled_listener_vec_):
            self.order_canceled_listener_vec_.append(_listener_)
    
    @staticmethod
    def GetUniqueInstance(watch_, smv):
        short_code = smv.shortcode()
        if short_code not in BaseSimMarketMaker.shcToSMMmap.keys():
            BaseSimMarketMaker.shcToSMMmap[short_code] = BaseSimMarketMaker(watch_, smv)
        return BaseSimMarketMaker.shcToSMMmap[short_code]
    
    def TimePeriodUpdate(self):
        if (self.all_requests_):
            self.ProcessRequestQueue(False)
    
    def Connect(self):
        t_server_assigned_client_id_ = len(self.client_position_map_)
        self.client_position_map_.append(0)
        #self.global_position_to_send_map_.append(self.global_position_)
        #self.masked_from_market_data_bids_map_.append(0)
        #self.masked_from_market_data_asks_map_.append(0)
        return t_server_assigned_client_id_
    
    def UpdateQueueSizes(self, _new_size_, _prev_size_, _order_):
        if (_new_size_ == _prev_size_):
            return
        if (_new_size_ < _prev_size_):
            _order_.queue_size_ahead_ -= int(_order_.queue_size_ahead_ * float((_prev_size_ - _new_size_)) / _prev_size_)
        _order_.queue_size_behind_ = _new_size_ - _order_.queue_size_ahead_
        _order_.num_events_seen_ += 1
            
    def FetchOrder(self, _buysell_, _int_price_, _server_assigned_order_sequence_):
        if (_buysell_ == 'B'):
            if (_int_price_ in self.intpx_to_bid_order_vec_.keys()):
                for order_ in self.intpx_to_bid_order_vec_[_int_price_]:
                    if (order_.server_assigned_order_sequence_ == _server_assigned_order_sequence_):
                        return order_
            for key_ in self.intpx_to_bid_order_vec_.keys():#this is because its price may have been reset
                for order_ in self.intpx_to_bid_order_vec_[key_]:
                    if (order_.server_assigned_order_sequence_ == _server_assigned_order_sequence_):
                        return order_
        else:
            if (_int_price_ in self.intpx_to_ask_order_vec_.keys()):
                for order_ in self.intpx_to_ask_order_vec_[_int_price_]:
                    if (order_.server_assigned_order_sequence_ == _server_assigned_order_sequence_):
                        return order_
            for key_ in self.intpx_to_ask_order_vec_.keys():
                for order_ in self.intpx_to_ask_order_vec_[key_]:
                    if (order_.server_assigned_order_sequence_ == _server_assigned_order_sequence_):
                        return order_
    
    def SendOrderExch(self, _server_assigned_client_id_, _security_name_, _buysell_, _price_, _size_requested_, _int_price_, _client_assigned_order_sequence_):
        #print 'SendOrderExch'
        order_ = BaseOrder()
        order_.security_name_ = _security_name_
        order_.buysell_ = _buysell_
        order_.price_ = _price_
        order_.size_remaining_ = _size_requested_
        order_.int_price_ = _int_price_
        order_.order_status_ = 'Conf'
        order_.size_requested_ = _size_requested_ # Check
        order_.num_events_seen_ = 0
        order_.client_assigned_order_sequence_ = _client_assigned_order_sequence_
        order_.server_assigned_order_sequence_ = self.server_assigned_order_sequence_
        order_.server_assigned_client_id_ = _server_assigned_client_id_
        self.server_assigned_order_sequence_ += 1
        # Not keeping masked_from_market_data_asks_map_ and alone_above_best_market
        if (order_.buysell_ == 'B'):
            order_.queue_size_behind_ = 0
            order_.queue_size_ahead_ = 0
            if (order_.int_price_ >= self.dep_market_view_.bestask_int_price()):
                order_.int_price_ = self.dep_market_view_.bestask_int_price()
                order_.price_ = self.dep_market_view_.bestask_price()
                if (self.dep_market_view_.bestask_size() >= order_.size_remaining()):
                    size_executed_ = order_.ExecuteRemaining()
                    self.client_position_map_[_server_assigned_client_id_] += size_executed_
                    #self.global_position_to_send_map_[_server_assigned_client_id_] += size_executed_
                    self.BroadcastExecNotification(_server_assigned_client_id_, order_)
                    print('executed')
                else:
                    size_executed_ = order_.MatchPartial(self.dep_market_view_.bestask_size())
                    self.client_position_map_[_server_assigned_client_id_] += size_executed_
                    #self.global_position_to_send_map_[_server_assigned_client_id_] += size_executed_
                    self.BroadcastExecNotification(_server_assigned_client_id_, order_)
                    if (not order_.int_price_ in self.intpx_to_bid_order_vec_.keys()):
                        self.intpx_to_bid_order_vec_[order_.int_price_] = []
                    self.intpx_to_bid_order_vec_[order_.int_price_].append(order_)
                    print('liquidity')
            else:
                #print 'Adding Buy Liquidity order'
                if (not order_.int_price_ in self.intpx_to_bid_order_vec_.keys()):
                    self.intpx_to_bid_order_vec_[order_.int_price_] = []
                self.intpx_to_bid_order_vec_[order_.int_price_].append(order_)
                print('liquidity')
        else:
            order_.queue_size_behind_ = 0
            order_.queue_size_ahead_ = 0
            if (order_.int_price_ <= self.dep_market_view_.bestbid_int_price()):
                order_.int_price_ = self.dep_market_view_.bestbid_int_price()
                order_.price_ = self.dep_market_view_.bestbid_price()
                if ((self.dep_market_view_.bestbid_size()) >= order_.size_remaining()):
                    size_executed = order_.ExecuteRemaining()
                    self.client_position_map_[_server_assigned_client_id_] -= size_executed
                    #self.global_position_to_send_map_[_server_assigned_client_id_] += size_executed
                    self.BroadcastExecNotification(_server_assigned_client_id_, order_)
                    print('executed')
                else:
                    size_executed_ = order_.MatchPartial(self.dep_market_view.bestbid_size())
                    self.client_position_map_[_server_assigned_client_id_] -= size_executed_
                    #self.global_position_to_send_map_[_server_assigned_client_id_] += size_executed_
                    self.BroadcastExecNotification(_server_assigned_client_id_, order_)
                    if (not order_.int_price_ in self.intpx_to_ask_order_vec_.keys()):
                        self.intpx_to_ask_order_vec_[order_.int_price_] = []
                    self.intpx_to_ask_order_vec_[order_.int_price_].append(order_)
                    print('liquidity')
            else:
                if (not order_.int_price_ in self.intpx_to_ask_order_vec_.keys()):
                    self.intpx_to_ask_order_vec_[order_.int_price_] = []
                self.intpx_to_ask_order_vec_[order_.int_price_].append(order_)
                print('liquidity')
        #order_.dump()
    
    def CancelOrderExch(self, _server_assigned_client_id_, _server_assigned_order_sequence_, _buysell_, _int_price_):
        order_ = self.FetchOrder(_buysell_, _int_price_, _server_assigned_order_sequence_)        
        if (order_.server_assigned_client_id_ == _server_assigned_client_id_):
            if (order_.CanBeCanceled()):
                if (_buysell_ == 'B'):
                    self.intpx_to_bid_order_vec_[order_.int_price_].remove(order_)
                else:
                    self.intpx_to_ask_order_vec_[order_.int_price_].remove(order_)
                self.BroadcastCancelNotification(_server_assigned_client_id_, order_)
        
    def OnMarketUpdate(self, _market_update_info_):
        self.count_ += 1
        print('SMM.OnMarketUpdate'),
        #print('SMM.keys: '), 
        #print self.intpx_to_bid_order_vec_.keys()
        for price_ in self.intpx_to_bid_order_vec_.keys():
            #print('SMM.price_: '+str(price_))
            #print('SMM.bestbid_int_price_: '+str(self.dep_market_view_.bestbid_int_price()))
            #print('SMM.bestask_int_price_: '+str(self.dep_market_view_.bestask_int_price()))

            if (price_ < self.dep_market_view_.bestbid_int_price()):
                continue
            order_vec_ = self.intpx_to_bid_order_vec_[price_]
            #print('order_vec_: '),
            #print(order_vec_)
            if (not order_vec_):
                continue
            #print('here')
            if (price_ >= self.dep_market_view_.bestask_int_price()):
                for order_ in order_vec_[:]:
                    available_size_for_exec_ = 999999 # Very high value
                    this_size_executed_ = 0
                    if (price_ == self.dep_market_view_.bestask_int_price()):
                        available_size_for_exec_ = self.dep_market_view_.bestask_size()
                    if (available_size_for_exec_ >= order_.size_remaining()):
                        this_size_executed_ = order_.ExecuteRemaining()
                    else:
                        this_size_executed_ = order_.MatchPartial(available_size_for_exec_)
                    self.client_position_map_[order_.server_assigned_client_id()] += this_size_executed_
                    #self.global_position_to_send_map_[order_.server_assigned_client_id()] += this_size_executed_
                    self.BroadcastExecNotification(order_.server_assigned_client_id(), order_)
                    if (order_.size_remaining() == 0):
                        order_vec_.remove(order_)
            elif (price_ > self.dep_market_view_.bestbid_int_price()):
                for order_ in order_vec_:
                    order_.Enqueue(0)
            else:
                #print('wtf')
                for order_ in order_vec_[:]:
                    #print('must be reached')
                    prev_size_ = order_.queue_size_behind_ + order_.queue_size_ahead_
                    new_size_ = self.dep_market_view_.bestbid_size()
                    if (order_.num_events_seen_ == 0): # first time
                        order_.queue_size_behind_ = 0
                        order_.queue_size_ahead_ = self.dep_market_view_.bestbid_size()
                        order_.num_events_seen_ = 1
                        #order_.dump()
                    else: # not the first time
                        self.UpdateQueueSizes(new_size_, prev_size_, order_)
                        #order_.dump()
    
        for price_ in self.intpx_to_ask_order_vec_.keys():
            if (price_ > self.dep_market_view_.bestask_int_price()):
                continue
            order_vec_ = self.intpx_to_ask_order_vec_[price_]
            if (not order_vec_):
                continue
            if (price_ <= self.dep_market_view_.bestbid_int_price()):
                for order_ in order_vec_:
                    available_size_for_exec_ = 999999 # Very high value
                    this_size_executed_ = 0
                    if (price_ == self.dep_market_view_.bestbid_int_price()):
                        available_size_for_exec_ = self.dep_market_view_.bestbid_size()
                    if (available_size_for_exec_ >= order_.size_remaining()):
                        this_size_executed_ = order_.ExecuteRemaining()
                    else:
                        this_size_executed_ = order_.MatchPartial(available_size_for_exec_)
                    self.client_position_map_[order_.server_assigned_client_id()] -= this_size_executed_
                    #self.global_position_to_send_map_[order_.server_assigned_client_id()] -= this_size_executed_
                    self.BroadcastExecNotification(order_.server_assigned_client_id(), order_)
                    if (order_.size_remaining() == 0):
                        order_vec_.remove(order_)
            elif (price_ < self.dep_market_view_.bestask_int_price()):
                for order_ in order_vec_:
                    order_.Enqueue(0)
            else:
                for order_ in order_vec_:
                    prev_size_ = order_.queue_size_behind_ + order_.queue_size_ahead_
                    new_size_ = self.dep_market_view_.bestask_size()
                    if (order_.num_events_seen_ == 0): # first time
                        order_.queue_size_behind_ = 0
                        order_.queue_size_ahead_ = self.dep_market_view_.bestask_size()
                        order_.num_events_seen_ = 1
                        #order_.dump()
                    else: # not the first time
                        self.UpdateQueueSizes(new_size_, prev_size_, order_)
                        #order_.dump()
        self.dump()
                
    def OnTradePrint(self, _trade_print_info_, _market_update_info_):
        print('SMM.OnTradePrint'),
        if (_trade_print_info_.buysell_ == 'B'):
            #askside_trade_size_ = _trade_print_info_.size_traded_
#             if (self.masked_asks_):
#                 self.masked_asks_ = False
#                 if (self.bestask_int_price_ == _trade_print_info_.int_trade_price_):
#                     for i in range(0, len(self.masked_from_market_data_asks_map_)):
#                         self.masked_from_market_data_asks_map_[i] = max(self.masked_from_market_data_asks_map_[i] - _trade_print_info_.size_traded_, 0)
#                         if (self.masked_from_market_data_asks_map_[i] > 0):
#                             masked_asks_ = True
#                 else:
#                     self.FillInValue(self.masked_from_market_data_asks_map_, 0)
    
            for price_ in self.intpx_to_ask_order_vec_.keys():
                if (price_ > _trade_print_info_.int_trade_price_):
                    continue
                order_vec_ = self.intpx_to_ask_order_vec_[price_]
                if (not order_vec_):
                    continue
                if (price_ < _trade_print_info_.int_trade_price_):
                    # Limit Ask Order at a higher level than Lift Price (currently not checking masks ... simply filling)
                    # non-zero orders at this price level
                    for order_ in order_vec_: # TODO: where is the watch_.tv condition?
                        this_size_executed_ = order_.ExecuteRemaining()
                        self.client_position_map_[order_.server_assigned_client_id()] -= this_size_executed_
                        #self.global_position_to_send_map_[order_.server_assigned_client_id()] -= this_size_executed_
                        self.BroadcastExecNotification(order_.server_assigned_client_id(), order_)
                    order_vec_ = []
                else:
                    # Limit Ask Order at a same level/price than Lift trade in market (Check to see if executed, and Enqueue if not finished)
                    # there are orders at this price level
                    # an estimate of the total_market_non_self_size at this level after this trade, we can use it to adjust queue_size_ahead_ and queue_size_behind_
                    if (self.dep_market_view_.bestask_int_price() > _trade_print_info_.int_trade_price_):
                        posttrade_asksize_at_trade_price_ = 0
                    else: 
                        posttrade_asksize_at_trade_price_ = self.dep_market_view_.bestask_size()
                    #for i in range(0, len(self.saci_to_executed_size_)):
                    #    self.saci_to_executed_size_[i] = 0
                    for order_ in order_vec_[:]:
                        # check which orders are executed, send message and deallocate order, nullify the pointer, erase from vector.
                        # Note the iterator does not need to be incremented since we either break out of loop or erase the iterator and hence increment it.
                        #trd_size_ = _trade_print_info_.size_traded_
                        trade_size_to_be_used_ = _trade_print_info_.size_traded_
                        #if (not self.dep_market_view_.trade_before_quote()):
                        #    trd_size_ = self.RestoreQueueSizes(order_, t_posttrade_asksize_at_trade_price_, trd_size_)
                        #trade_size_to_be_used_ = _trade_print_info_.size_traded_ - self.saci_to_executed_size_[order_.server_assigned_client_id()]
                        #if (trade_size_to_be_used_ <= 0):
                        #    continue
                        t_size_executed_ = order_.HandleCrossingTrade(trade_size_to_be_used_, posttrade_asksize_at_trade_price_)
                        if (t_size_executed_ > 0):
                            self.client_position_map_[order_.server_assigned_client_id()] -= t_size_executed_
                            #self.global_position_to_send_map_[order_.server_assigned_client_id()] -= t_size_executed_
                            #self.saci_to_executed_size_[order_.server_assigned_client_id()] += t_size_executed_
                            self.BroadcastExecNotification (order_.server_assigned_client_id(), order_)
                            if (order_.size_remaining() <= 0):
                                order_vec_.remove(order_)
    
        else:
            # trade was a HIT, i.e. removing liquidity on the bid side
            #bidside_trade_size_ = _trade_print_info_.size_traded_
#             if (self.masked_bids_):
#                 self.masked_bids_ = False
#                 if (self.bestbid_int_price_ == _trade_print_info_.int_trade_price_):
#                     for i in range(0, self.masked_from_market_data_bids_map_):
#                         self.masked_from_market_data_bids_map_[i] = max(self.masked_from_market_data_bids_map_[i] - _trade_print_info_.size_traded_, 0)
#                         if (self.masked_from_market_data_bids_map_[ i ] > 0):
#                             self.masked_bids_ = True
#                 else:
#                     self.FillInValue(self.masked_from_market_data_bids_map_, 0)
    
            for price_ in self.intpx_to_bid_order_vec_.keys():
                if (price_ < _trade_print_info_.int_trade_price_):
                    continue
                order_vec_ = self.intpx_to_bid_order_vec_[price_]
                if (not order_vec_):
                    continue
                if (price_ > _trade_print_info_.int_trade_price_):
                    # Aggressive Order at a lower level ( currently not checking masks ... simply filling )
                    for order_ in order_vec_[:]:
                        this_size_executed_ = order_.ExecuteRemaining()
                        self.client_position_map_[order_.server_assigned_client_id()] += this_size_executed_
                        #self.global_position_to_send_map_[order_.server_assigned_client_id()] += this_size_executed_
                        self.BroadcastExecNotification(order_.server_assigned_client_id(), order_)
                    order_vec_ = []
                else:
                    # ( i2bov_iter_->first == _trade_print_info_.int_trade_price_ ) ... trade at best-nonself-market. Check to see if executed, and Enqueue if not finished
                    # an estimate of the total_market_non_self_size at this level after this trade, we can use it to adjust queue_size_ahead_ and queue_size_behind_
                    if (self.dep_market_view_.bestbid_int_price() < _trade_print_info_.int_trade_price_):
                        posttrade_bidsize_at_trade_price_ = 0
                    else: 
                        posttrade_bidsize_at_trade_price_ = self.dep_market_view_.bestbid_size()
                    # an estimate of the total_market_non_self_size at this level after this trade, we can use it to adjust queue_size_ahead_ and queue_size_behind_    
                    #for i in range(0, len(self.saci_to_executed_size_)):
                    #    self.saci_to_executed_size_[ i ] = 0
                    for order_ in order_vec_[:]:
                        # check which orders are executed, send message and deallocate order, nullify the pointer, erase from vector.
                        # Note the iterator does not need to be incremented since we either break out of loop or erase the iterator and hence increment it.
                        #trade_size_to_be_used_ = _trade_print_info_.size_traded_ - self.saci_to_executed_size_[order_.server_assigned_client_id()]
                        #if (trade_size_to_be_used_ <= 0):
                        #    continue
                        #trd_size_ = _trade_print_info_.size_traded_
                        trade_size_to_be_used_ = _trade_print_info_.size_traded_
                        t_size_executed_ = order_.HandleCrossingTrade(trade_size_to_be_used_, posttrade_bidsize_at_trade_price_)
                        if (t_size_executed_ > 0):
                            self.client_position_map_[order_.server_assigned_client_id()] += t_size_executed_
                            #self.global_position_to_send_map_ [order_.server_assigned_client_id ( ) ] += t_size_executed_
                            #self.saci_to_executed_size_[order_.server_assigned_client_id ( ) ] += t_size_executed_
                            self.BroadcastExecNotification(order_.server_assigned_client_id(), order_)
                            if (order_.size_remaining() <= 0):
                                order_vec_.remove(order_)
        self.dump()
    
    def OnTimePeriodUpdate(self, num_pages_to_add_):
        return
    
    def BroadcastExecNotification(self, _server_assigned_client_id_, _order_):
        print('BroadcastExecNotification '+str(self.client_position_map_[_server_assigned_client_id_]))
        for listener_ in self.order_executed_listener_vec_:
            listener_.OrderExecuted(_order_.server_assigned_client_id(), _order_.client_assigned_order_sequence(),
                                    _order_.server_assigned_order_sequence(), self.dep_market_view_.shortcode_, 
                                    _order_.price_, _order_.buysell(), _order_.size_remaining(), _order_.size_executed(),
                                    self.client_position_map_[_server_assigned_client_id_],
                                    self.client_position_map_[_server_assigned_client_id_], _order_.int_price_)
            
    def BroadcastCancelNotification(self, _server_assigned_client_id_, _order_):
        print('BroadcastCancelNotification')
        print self.order_canceled_listener_vec_
        for listener_ in self.order_canceled_listener_vec_:
            listener_.OrderCanceled(_order_.server_assigned_client_id(), _order_.client_assigned_order_sequence(),
                                    _order_.server_assigned_order_sequence(), self.dep_market_view_.shortcode_, 
                                    _order_.price_, _order_.buysell(), _order_.size_remaining(), _order_.size_executed(),
                                    self.client_position_map_[_server_assigned_client_id_],
                                    self.client_position_map_[_server_assigned_client_id_], _order_.int_price_)