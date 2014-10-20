from OrderManager.base_order import BaseOrder
from MarketAdapter.security_market_view_change_listener import SecurityMarketViewChangeListener
from ExternalData.external_time_listener import TimePeriodListener
from OrderManager.request import Request
        

class BaseSimMarketMaker(SecurityMarketViewChangeListener, TimePeriodListener):
    
    shcToSMMmap = dict()

    '''constructor'''
    def __init__(self, _watch_, _smv_):
        
        self.global_position_ = 0
        self.client_position_map_ = []
        self.global_position_to_send_map_ = []
        self.masked_asks_ = False
        self.masked_bids_ = False
        self.masked_from_market_data_bids_map_ = []
        self.masked_from_market_data_asks_map_ = []
        self.watch_ = _watch_
        self.all_requests_ = []
        self.pending_requests_ = []
        self.all_requests_lock_ = False
        
        self.intpx_to_ask_order_vec_ = {}
        self.intpx_to_bid_order_vec_ = {}
        
        self.dep_market_view_ = _smv_
        self.bestbid_int_price_ = 0
        self.bestask_int_price_ = 0 
        self.bestbid_size_ = 0
        self.bestask_size_ = 0
        self.last_bid_size_change_msecs_ = 0
        self.last_ask_size_change_msecs_ = 0
        self.ask_side_priority_order_exists_ = False
        self.ask_side_priority_order_size_ = 0
        self.bid_side_priority_order_exists_ = False
        self.bid_side_priority_order_size_ = 0
        self.dep_market_view_.SubscribePriceType(self, "MktSizeWPrice")
        self.watch_.SubscribeBigTimePeriod(self) # may make small Time period also in watch
        
        self.server_assigned_order_sequence_ = 0
        self.saos_to_seqd_time_ = [] # server_assigned_order_sequence
        
        self.order_rejection_listener_vec_ = []
        self.order_sequenced_listener_vec_ = []
        
        self.saci_to_executed_size_ = []
        
        return
    
    @staticmethod
    def GetUniqueInstance(watch_, smv):
        short_code = smv.shortcode()
        if short_code not in BaseSimMarketMaker.shcToSMMmap.keys():
            BaseSimMarketMaker.shcToSMMmap[short_code] = BaseSimMarketMaker(watch_, smv)
        return BaseSimMarketMaker.shcToSMMmap[short_code]
    
    def Connect(self):
        t_server_assigned_client_id_ = len(self.client_position_map_)
        self.client_position_map_.append(0)
        self.global_position_to_send_map_.append(self.global_position_)
        self.masked_from_market_data_bids_map_.append(0)
        self.masked_from_market_data_asks_map_.append(0)
        return t_server_assigned_client_id_
    
    '''If an order exists in order_book, returns it otherwise returns None '''
    def FetchOrder(self, _buysell_, _int_price_, _server_assigned_order_sequence_):
        if (_buysell_ == 1):
            if (_int_price_ in self.int_price_to_bid_order_vec.keys()):
                for order in self.int_price_to_bid_order_vec[_int_price_]:
                    if (order.server_assigned_order_sequence == _server_assigned_order_sequence_):
                        return order
            for key in self.int_price_to_bid_order_vec.keys():
                for order in self.int_price_to_bid_order_vec[key]:
                    if (order.server_assigned_order_sequence == _server_assigned_order_sequence_):
                        return order
        else:
            if (_int_price_ in self.int_price_to_ask_order_vec.keys()):
                for order in self.int_price_to_bid_order_vec[_int_price_]:
                    if (order.server_assigned_order_sequence == _server_assigned_order_sequence_):
                        return order
            for key in self.int_price_to_ask_order_vec.keys():
                for order in self.int_price_to_ask_order_vec[key]:
                    if (order.server_assigned_order_sequence == _server_assigned_order_sequence_):
                        return order
    
    def AddRequest(self, _request_):
        if (self.all_requests_lock_):
            self.pending_requests_.append(_request_)
        else:
            self.all_requests_.append(_request_)
            self.all_requests_.sort() #stable_sort(self.all_requests) # Corrected this)
    
    #We might need bool variable so that we can keep the cancel request on next time update.. 
    def ProcessRequestQueue(self, find_out_why_): # Later find out whether that boolean variable is needed
        if (self.all_requests_lock_):
            return
        self.all_requests_lock_ = True
        for request in self.all_requests_:
            server_assigned_client_id_ = request.server_assigned_client_id_
            if (request.wakeup_time_ > self.watch_.tv()):
                continue
            if (request.request_type_ == "SEND"):
                order = request.order_
                # This order will always get confirmed
                order.Confirm()
                # Broadcast this information
                if (order.buysell_ == 'B'): # Buy
                    
                    # Bid side order         
                    # Update queue sizes
                    order.queue_size_behind_ = 0
                    order.queue_size_ahead_ = self.dep_market_view_.bid_size_at_int_price(order.int_price) # How? TODO:
                    
                    # Check if aggressive
                    if (order.int_price >= self.dep_market_view_.bestask_int_price()):
                        # Reset to the best ask level
                        order.int_price = self.dep_market_view_.bestask_int_price()
                        order.price = self.dep_market_view_.bestask_price()
                        
                        # Execute the order, update position, send Exec
                        if (self.dep_market_view_.bestask_size() - self.masked_from_market_data_asks_map_[order.server_assigned_client_id_] > 0):
                            if ((self.dep_market_view_.bestask_size() - self.masked_from_market_data_asks_map_[order.server_assigned_client_id_]) >= order.size_remaining()):
                                # Full execution
                                size_executed = order.ExecuteRemaining()
                                self.client_position_map_[server_assigned_client_id_] += size_executed
                                self.global_position_to_send_map_[server_assigned_client_id_] += size_executed

                                # BroadcastExecNotification ( r_server_assigned_client_id_, p_new_sim_order_ ) ;
                                self.masked_from_market_data_asks_map_[server_assigned_client_id_] += size_executed
                                self.masked_asks = True
                            else:
                                # Partial execution
                                size_executed = order.MatchPartial(self.dep_market_view_.bestask_size()-self.masked_from_market_data_asks_map_[server_assigned_client_id_])
                                self.client_position_map_[server_assigned_client_id_] += size_executed
                                self.global_position_to_send_map_[server_assigned_client_id_] += size_executed

                                # BroadcastExecNotification ( r_server_assigned_client_id_, p_new_sim_order_ ) ;
                                self.masked_from_market_data_asks_map_[server_assigned_client_id_] += size_executed
                                self.masked_asks = True

                                self.intpx_to_bid_order_vec_[order.int_price_].append(order)
                                if (order.int_price_ > self.dep_market_view_.bestbid_int_price()):
                                    order.alone_above_best_market_ = True
                    else:
                        # Add liquidity order
                        self.intpx_to_bid_order_vec_[order.int_price_].append(order)
                        if (order.int_price_ > self.dep_market_view_.bestbid_int_price()):
                            order.alone_above_best_market_ = True
                else:
                    
                    # Ask side order
                    # Update queue sizes
                    order.queue_size_behind_ = 0
                    order.queue_size_ahead_ = self.dep_market_view_.asksize_at_int_price(order.int_price)
                    
                    # Check if aggressive
                    if (order.int_price <= self.dep_market_view_.bestbid_int_price()):
                        # Reset to the best ask level
                        order.int_price = self.dep_market_view_.bestbid_int_price()
                        order.price = self.dep_market_view_.bestbid_price()
                        
                        # Execute the order, update position, send Exec
                        if (self.dep_market_view_.bestbid_size()-self.masked_from_market_data_bids_map_[order.server_assigned_client_id_] > 0):
                            if ((self.dep_market_view_.bestbid_size()-self.masked_from_market_data_bids_map_[order.server_assigned_client_id_]) >= order.size_remaining()):
                                # Full execution
                                size_executed = order.ExecuteRemaining()
                                self.client_position_map_[server_assigned_client_id_] += size_executed
                                self.global_position_to_send_map_[server_assigned_client_id_] += size_executed

                                # BroadcastExecNotification ( r_server_assigned_client_id_, p_new_sim_order_ ) ;
                                self.masked_from_market_data_bids_map_[server_assigned_client_id_] += size_executed
                                self.masked_asks_ = True
                            else:
                                # Partial execution
                                size_executed = order.MatchPartial(self.dep_market_view.bestbid_size()-self.masked_from_market_data_asks_map[server_assigned_client_id_])
                                self.client_position_map_[server_assigned_client_id_] += size_executed
                                self.global_position_to_send_map_[server_assigned_client_id_] += size_executed

                                # BroadcastExecNotification ( r_server_assigned_client_id_, p_new_sim_order_ ) ;
                                self.masked_from_market_data_bids_map_[server_assigned_client_id_] += size_executed
                                self.masked_asks_ = True

                                self.intpx_to_ask_order_vec_[order.int_price_].append(order)
                                if (order.int_price_ > self.dep_market_view_.bestask_int_price()):
                                    order.alone_above_best_market_ = True
                    else:
                        # Add liquidity order
                        if (not order.int_price_ in self.intpx_to_ask_order_vec_.keys()):
                            self.intpx_to_ask_order_vec_[order.int_price_] = []
                        self.intpx_to_ask_order_vec_[order.int_price_].append(order)
                        if (order.int_price_ > self.dep_market_view_.bestask_int_price()):
                            order.alone_above_best_market_ = True
                            
            elif (request.request_type == "CANCEL"):
                if (self.process_only_sendtrades_):
                    return
                to_postpone = 0
                server_assigned_order_sequence = request.sreq_.scor_.server_assigned_order_sequence_
                buysell = request.sreq_.scor_.buysell
                int_price = request.sreq_.scor_.int_price_

                order = self.FetchOrder(buysell, int_price, server_assigned_order_sequence)

                # Probably only the first condition is required
                if (order is not None and (order.server_assigned_client_id == server_assigned_client_id_)):
                    if (buysell == 1):
                        if (not request.postponed_once):
                            # if never postponed then see if it needs to be postponed
                            if (order.int_price < self.dep_market_view.bestbid_int_price()):
                                # not best market
                                pass
                            elif (order.int_price == self.dep_market_view.bestbid_int_price()):
                                # at best market
                                if ((order.num_events_seen() < 1) and (not order.IsConfirmed())):
                                    # order has seen less than 1 event or is not even confirmed yet
                                    to_postpone = 1
                            else:
                                if (order.num_events_seen() < 5):
                                    to_postpone = 2
                                else:
                                    if (self.dep_market_view.SpreadWiderThanNormal()):
                                        to_postpone = 3
                        if (order.IsExecuted()):
                            # Prematurely executed, just waiting on the OnTradePrint call.
                            to_postpone = 4
                        if (to_postpone == 0):
                            pass
                            #UniqueVectorRemove(self.int_price_to_bid_order_vec[order.int_price], order)
                            #BroadcastCancelNotification(r_server_assigned_client_id, order)
                        else:
                            pass
                    else:
                        if (not request.postponed_once):
                            # if never postponed then see if it needs to be postponed
                            if (order.int_price > self.dep_market_view.bestask_int_price()):
                                # not best market
                                pass
                            elif (order.int_price() == self.dep_market_view.bestask_int_price()):
                                # at best market
                                if ((order.num_events_seen() < 1) and (not order.IsConfirmed())):
                                    # order has seen less than 1 event or is not even confirmed yet
                                    to_postpone = 1
                            else:
                                # above best market
                                if (order.num_events_seen() < 5):
                                    to_postpone = 2
                                else:
                                    if (self.dep_market_view.SpreadWiderThanNormal()):
                                        to_postpone = 3

                        if (order.IsExecuted()):
                            # Prematurely executed , just waiting on the OnTradePrint call.
                            to_postpone = 4
                        if (to_postpone == 0):
                            '''Need to mae __eq__ () function for order'''
                            #UniqueVectorRemove (int_price_to_ask_order_vec[order.int_price], order)
                            #BroadcastCancelNotification(r_server_assigned_client_id_, order)
                            pass
        
        if (self.pending_requests_):
            for request in self.pending_requests_:
                self.all_requests.append(request)
            self.pending_requests_ = []
        self.all_requests_lock_ = False    
    
    def SendOrderExch(self, _server_assigned_client_id_, _security_name_, _buysell_, _price_, _size_requested_, _int_price_, _client_assigned_order_sequence_):
        print 'SendOrderExch'
        order_ = BaseOrder()
        order_.security_name_ = _security_name_
        order_.buysell_ = _buysell_
        order_.price_ = _price_
        order_.size_remaining_ = _size_requested_
        order_.int_price_ = _int_price_
        order_.order_status_ = 0 # Not Needed
        order_.size_requested_ = _size_requested_ # Check
        order_.queue_size_ahead_ = 0
        order_.queue_size_behind_ = 0
        
        order_.num_events_seen_ = 0
        order_.client_assigned_order_sequence_ = _client_assigned_order_sequence_
        order_.server_assigned_order_sequence_ = self.server_assigned_order_sequence_
        self.server_assigned_order_sequence_ += 1
        
        order_.server_assigned_client_id_ = _server_assigned_client_id_
        
        order_.order_sequenced_time_ = self.watch_.tv()
        
        # Size requested must be a multiple of MinOrderSize
        if (not _size_requested_ % self.dep_market_view_.MinOrderSize() != 0):
            # Broadcast rejection
            self.BroadcastRejection(_server_assigned_client_id_, order_, 'kSendOrderRejectNotMinOrderMultiple')
            
        self.saos_to_seqd_time_.append(self.watch_.tv())
        self.server_assigned_order_sequence_ += 1
        # Broadcast sequenced
        self.BroadcastSequenced(_server_assigned_client_id_, order_)
        
        order_.dump()
        
        # Create a request class
        new_request_ = Request()
        new_request_.wakeup_time_ = self.watch_.tv()
        new_request_.request_type_ = 'SEND'
        new_request_.order_ = order_
        new_request_.server_assigned_client_id_ = _server_assigned_client_id_        
        self.AddRequest(new_request_)
    
    def CancelOrderExch(self, _server_assigned_client_id_, _server_assigned_order_sequence_, _buysell_, _int_price_):
        '''Cancellation logic here'''
        new_request_ = Request()
        new_request_.wakeup_time = self.watch_.tv()
        new_request_.request_type = 'CANCEL'
        new_request_.order.buysell_ = _buysell_
        new_request_.order.int_price_ = _int_price_
        new_request_.server_assigned_client_id_ = _server_assigned_client_id_
        new_request_.server_assigned_order_sequence_ = _server_assigned_order_sequence_
        new_request_.postpone_once = False
        self.AddRequest(new_request_)
    
    def CancelReplaceOrderExch(self, _server_assigned_client_id_, _server_assigned_order_sequence_, _buysell_, _int_price_, _new_size_requested_):
        '''Replace logic here'''
        new_request_ = Request()
        new_request_.wakeup_time_ = self.watch_.tv()
        new_request_.request_type_ = 'REPLACE'
        new_request_.order.buysell_ = _buysell_
        new_request_.order.int_price_ = _int_price_
        new_request_.server_assigned_client_id_ = _server_assigned_client_id_
        new_request_.server_assigned_order_sequence_ = _server_assigned_order_sequence_
        new_request_.order.size_remaining_ = _new_size_requested_
        new_request_.postpone_once_ = False
        self.AddRequest(new_request_)
    
    def ReplayOrderExch(self, _server_assigned_client_id_, _client_assigned_order_sequence_, _buysell_, _int_price_, _server_assigned_order_sequence_):
        #not adding relpay now...
        return
    
    '''Broadcast Messages'''
    def BroadcastRejection(self, _server_assigned_client_id_, _order_, _order_rejection_reason_):
        for t_item_ in self.order_rejection_listener_vec_:
            t_item_.OrderRejected(_server_assigned_client_id_, _order_.client_assigned_order_sequence(), 
                                  self.dep_shortcode_, _order_.price(), _order_.buysell(), 
                                  _order_.size_remaining(), _order_rejection_reason_, _order_.int_price())
            
    # Add Client position
    def BroadcastSequenced(self, _server_assigned_client_id_, _order_):
        for t_item_ in self.order_sequenced_listener_vec_:
            t_item_.OrderRejected(_server_assigned_client_id_, _order_.client_assigned_order_sequence(), 
                                  _order_.server_assigned_order_sequence_, self.dep_shortcode_, _order_.price(), 
                                  _order_.buysell(), _order_.size_remaining(), _order_.size_executed(), 
                                  _order_.int_price())
            
    def OnMarketUpdate(self, _market_update_info_):
        return
        # Saving old values (required only for CFE): for matching trades with market quotes
        old_bestbid_int_price_ = self.bestbid_int_price_
        old_bestbid_size_ = self.bestbid_size_
        old_bestask_int_price_ = self.bestask_int_price_
        old_bestask_size_ = self.bestask_size_
    
        if (self.bestbid_size_ < _market_update_info_.bestbid_size_):
            last_bid_size_change_msecs_ = self.watch_.GetMsecsFromMidnight()
    
        if (self.bestask_size_ < _market_update_info_.bestask_size_):
            last_ask_size_change_msecs_ = self.watch_.GetMsecsFromMidnight() ;
    
        if (old_bestask_int_price_ > _market_update_info_.bestask_int_price_): 
            if (self.dep_market_view_.ask_order(0) == 1):
                self.FillInValue(self.ask_side_priority_order_exists_map_, True)
                self.FillInValue(self.ask_side_priority_order_size_map_ , self.dep_market_view_.ask_size(0))
            else:
                self.FillInValue(self.ask_side_priority_order_exists_map_, False)
                self.FillInValue(self.ask_side_priority_order_size_map_, 0)
    
        if (old_bestbid_int_price_ < _market_update_info_.bestbid_int_price_): 
            if (self.dep_market_view_.bid_order(0) == 1):
                self.FillInValue(self.bid_side_priority_order_exists_map_, True)
                self.FillInValue(self.bid_side_priority_order_size_map_, self.dep_market_view_.bid_size(0))
            else:
                self.FillInValue(self.bid_side_priority_order_exists_map_, False)
                self.FillInValue(self.bid_side_priority_order_size_map_, 0)
    
        # currently strictly removing rhe proority order if queue size changes
        # Can change if sim -real is still bad 
        if (old_bestask_int_price_ == self.dep_market_view_.ask_int_price (0) and old_bestask_size_ > self.dep_market_view_.ask_size(0)):
            self.FillInValue(self.ask_side_priority_order_exists_map_, False)
            self.FillInValue(self.ask_side_priority_order_size_map_, 0)
    
        if (old_bestbid_int_price_  == self.dep_market_view_.bid_int_price( 0 ) and old_bestbid_size_ > self.dep_market_view_.bid_size(0) ):
            self.FillInValue(self.bid_side_priority_order_exists_map_, False)
            self.FillInValue(self.bid_side_priority_order_size_map_, 0)
    
        if (self.sid_to_sim_config_[self.dep_security_id_].use_aggressor_side_estimate_):
            if (not self.dep_market_view_.IsBidBookEmpty()):
                if (not self.last_bestbid_int_price_[0]):
                    # first time
                    self.last_bestbid_int_price_[0] = self.dep_market_view_.bid_int_price(0)
                if (not self.last_bestbid_int_price_[1]):
                    # first time
                    self.last_bestbid_int_price_[1] = self.dep_market_view_.bid_int_price(0)
                if (self.last_bestbid_int_price_[0] != self.dep_market_view_.bid_int_price(0)):
                    self.last_bestbid_int_price_[1] = self.last_bestbid_int_price_[0]
                    self.last_bestbid_int_price_[0] = self.dep_market_view_.bid_int_price(0)
            if (not self.dep_market_view_.IsAskBookEmpty()):
                if (not self.last_bestask_int_price_[0]):
                    # first time
                    self.last_bestask_int_price_[0] = self.dep_market_view_.ask_int_price(0)
                if (not self.last_bestask_int_price_[1]):
                    # first time
                    self.last_bestask_int_price_[1] = self.dep_market_view_.ask_int_price(0)
                if (not self.last_bestask_int_price_ [0] == self.dep_market_view_.ask_int_price(0)):
                    self.last_bestask_int_price_[1] = self.last_bestask_int_price_[0]
                    self.last_bestask_int_price_[0] = self.dep_market_view_.ask_int_price(0)
        if (self.sid_to_sim_config_ [self.dep_security_id_].max_conf_orders_above_best_level_ >= 0):
            self.CxlOrdersAboveBestLevel(self.sid_to_sim_config_[self.dep_security_id_].max_conf_orders_above_best_level_)
    
        if (self.all_requests_):
            self.ProcessRequestQueue(False)
    
        # TODO check if best market changed and if it changed on the bid side then clear masked_from_market_data_bids_map_, if ask best level 
        # changed then clear masked_from_market_data_asks_map_
        if (self.sid_to_sim_config_[self.dep_security_id_].using_only_full_mkt_for_sim_):
            if (not self.bestbid_int_price_ == self.dep_market_view_.bid_int_price(0)):
                bestbid_int_price_ = self.dep_market_view_.bid_int_price(0)
                # reset masks on the bidside
                if (self.masked_bids_):
                    # this means that masks had been set, hence the need to unmask
                    self.FillInValue(self.masked_from_market_data_bids_map_, 0)
            bestbid_size_ = self.dep_market_view_.bid_size(0)
        else:
            if (not bestbid_int_price_ == self.dep_market_view_.market_update_info_.bestbid_int_price_):
                bestbid_int_price_ = self.dep_market_view_.market_update_info_.bestbid_int_price_;
                # reset masks on the bidside
                if (self.masked_bids_):
                    # this means that masks had been set, hence the need to unmask
                    self.FillInValue(self.masked_from_market_data_bids_map_, 0)
            bestbid_size_ = self.dep_market_view_.market_update_info_.bestbid_size_
    
        if (self.sid_to_sim_config_[self.dep_security_id_].using_only_full_mkt_for_sim_):
            if (not self.bestask_int_price_ == self.dep_market_view_.ask_int_price(0)):
                bestask_int_price_ = self.dep_market_view_.ask_int_price(0)
                # reset masks on the askside
                if (self.masked_asks_):
                    # this means that masks had been set, hence the need to unmask
                    self.FillInValue(self.masked_from_market_data_asks_map_, 0)
            bestask_size_ = self.dep_market_view_.ask_size(0)
        else:
            if (not bestask_int_price_ == self.dep_market_view_.market_update_info_.bestask_int_price_):
                bestask_int_price_ = self.dep_market_view_.market_update_info_.bestask_int_price_
                # reset masks on the askside
                if (self.masked_asks_):
                    # this means that masks had been set, hence the need to unmask
                    self.FillInValue(self.masked_from_market_data_asks_map_, 0)
            bestask_size_ = self.dep_market_view_.market_update_info_.bestask_size_
    
        if (self.sid_to_sim_config_[self.dep_security_id_].use_tgt_sim_market_maker_ or self.sid_to_sim_config_[self.dep_security_id_].use_baseprice_tgt_sim_market_maker_):
            flag = True
            prev_dep_price_change_ = self.p_dep_price_change_indicator_.indicator_value(flag)
    
        # Check if any orders have become aggressive if so fill them
        # Call Enqueue on orders at or above best market
        for price_ in self.intpx_to_bid_order_vec_.keys():
            if (price_ <= bestbid_int_price_):
                continue
            order_vec_ = self.intpx_to_bid_order_vec_[price_]
            if (price_ >= bestask_int_price_):
                # Possibly aggressive order ( currently not checking masks .. simply filling ! )
                if (order_vec_):
                    # non zero orders at this price level
                    for order_ in order_vec_[:]:
                        available_size_for_exec_ = 999999 # Very high value
                        this_size_executed_ = 0
                        if (price_ == bestask_int_price_):
                            available_size_for_exec_ = max(bestask_size_ - self.masked_from_market_data_asks_map_[order_.server_assigned_client_id()], 0)
                        if (available_size_for_exec_ >= order_.size_remaining()):
                            this_size_executed_ = order_.ExecuteRemaining()
                        else:
                            this_size_executed_ = order_.MatchPartial(available_size_for_exec_)
                        self.client_position_map_[order_.server_assigned_client_id()] += this_size_executed_
                        self.global_position_to_send_map_[order_.server_assigned_client_id()] += this_size_executed_
                        self.masked_from_market_data_asks_map_[order_.server_assigned_client_id()] += this_size_executed_
                        self.masked_asks_ = True
                        self.BroadcastExecNotification(order_.server_assigned_client_id(), order_)
                        if (order_.size_remaining() == 0):
                            order_vec_.remove(order_)
            elif (price_ > bestbid_int_price_): # above best nonself market ... Enqueue ( 0 )
                for order_ in order_vec_:
                    order_.Enqueue(0)
            elif (price_ == bestbid_int_price_): # at best nonself market ... To Enqueue
                for order_ in order_vec_[:]:
                    if (order_ is None):
                        continue
                    prev_size_ = order_.queue_size_behind_ + order_.queue_size_ahead_
                    if (self.sid_to_sim_config_[self.dep_security_id_].using_only_full_mkt_for_sim_):
                        new_size_ = self.dep_market_view_.bid_size(0)
                    else: 
                        new_size_ = self.dep_market_view_.market_update_info_.bestbid_size_
                    if (self.sid_to_sim_config_[self.dep_security_id_ ].using_only_full_mkt_for_sim_):
                        new_ordercount_ = self.dep_market_view_.bid_order(0)
                    else: 
                        new_ordercount_ = self.dep_market_view_.market_update_info_.bestbid_ordercount_
                    if (not self.dep_market_view_.trade_before_quote() and (not new_size_ == prev_size_ or order_.num_events_seen_ == 1)):
                        self.BackupQueueSizes(order_)
                    if (order_.num_events_seen_ == 0): # first time ... before this do not fill
                        order_.queue_size_behind_ = 0
                        if (self.sid_to_sim_config_[self.dep_security_id_ ].using_only_full_mkt_for_sim_):
                            order_.queue_size_ahead_ = self.dep_market_view_.bid_size(0)
                        else: 
                            self.dep_market_view_.market_update_info_.bestbid_size_
                        order_.num_events_seen_ = 1
                    else: # not the first time
                        if (self.sid_to_sim_config_[self.dep_security_id_].use_tgt_sim_market_maker_):
                            self.UpdateQueueSizesTargetPrice(new_size_, prev_size_, order_)
                        elif (self.sid_to_sim_config_[self.dep_security_id_].use_baseprice_tgt_sim_market_maker_):
                            self.UpdateQueueSizesBasePriceBasedTargetPrice(new_size_, prev_size_, order_)
                        elif (self.sid_to_sim_config_[self.dep_security_id_].use_fgbm_sim_market_maker_):
                            self.UpdateQueueSizesTradeBased(new_size_, prev_size_, order_)
                        else:
                            self.UpdateQueueSizes(new_size_, prev_size_, order_)
            elif (self.sid_to_sim_config_[self.dep_security_id_].adjust_non_best_order_queues_):
                for order_ in order_vec_:
                    if (order_ is None):
                        continue
                    prev_size_ = order_.queue_size_behind_ + order_.queue_size_ahead_
                    if (self.sid_to_sim_config_[self.dep_security_id_].using_only_full_mkt_for_sim_):
                        new_size_ = self.dep_market_view_.bid_size(0)
                    else: 
                        new_size_ = self.dep_market_view_.market_update_info_.bestbid_size_
                    if (not self.dep_market_view_.trade_before_quote() and (not new_size_ == prev_size_ or order_.num_events_seen_ == 1)):
                        self.BackupQueueSizes(order_)
                    if (order_.num_events_seen_ == 0): # first time ... before this do not fill
                        order_.queue_size_behind_ = 0
                        if (self.sid_to_sim_config_[self.dep_security_id_ ].using_only_full_mkt_for_sim_):
                            order_.queue_size_ahead_ = self.dep_market_view_.bid_size(0)
                        else:
                            order_.queue_size_ahead_ = self.dep_market_view_.market_update_info_.bestbid_size_
                        order_.num_events_seen_ = 1
                    else: # not the first time
                        if (self.sid_to_sim_config_[self.dep_security_id_ ].use_tgt_sim_market_maker_):
                            self.UpdateQueueSizesTargetPrice(new_size_, prev_size_, order_)
                        elif (self.sid_to_sim_config_[self.dep_security_id_].use_baseprice_tgt_sim_market_maker_):
                            self.UpdateQueueSizesBasePriceBasedTargetPrice ( new_size_ , prev_size_, order_)
                        elif (self.sid_to_sim_config_[self.dep_security_id_].use_fgbm_sim_market_maker_):
                            self.UpdateQueueSizesTradeBased(new_size_, prev_size_, order_)
                        else:
                            self.UpdateQueueSizes(new_size_, prev_size_, order_)
            else:
                break
    
        for price_ in self.intpx_to_ask_order_vec_.keys():
            order_vec_ = self.intpx_to_ask_order_vec_[price_]
            if (price_ <= bestbid_int_price_):
                # Possibly aggressive order ( currently not checking masks .. simply filling ! )
                if (order_vec_):
                    # non zero orders at this price level
                    for order_ in order_vec_:
                        available_size_for_exec_ = 999999; # Very high value
                        this_size_executed_ = 0
                        if (price_ == bestbid_int_price_):
                            available_size_for_exec_ = max(bestbid_size_ - self.masked_from_market_data_bids_map_[order_.server_assigned_client_id()], 0)
                        if (available_size_for_exec_ >= order_.size_remaining()):
                            this_size_executed_ = order_.ExecuteRemaining()
                        else:
                            this_size_executed_ = order_.MatchPartial(available_size_for_exec_)
                        self.client_position_map_[order_.server_assigned_client_id()] -= this_size_executed_
                        self.global_position_to_send_map_[order_.server_assigned_client_id()] -= this_size_executed_
                        self.masked_from_market_data_bids_map_[order_.server_assigned_client_id()] += this_size_executed_
                        self.masked_bids_ = True
                        self.BroadcastExecNotification(order_.server_assigned_client_id(), order_)
                        if (order_.size_remaining() == 0):
                            order_vec_.remove(order_)
            elif (price_ < bestask_int_price_):
                for order_ in order_vec_:
                    order_.Enqueue(0)
            elif (price_ == bestask_int_price_): # at best nonself market ... To Enqueue
                for order_ in order_vec_:
                    if (order_ is None):
                        continue
                    prev_size_ = order_.queue_size_behind_ + order_.queue_size_ahead_
                    if (self.sid_to_sim_config_[self.dep_security_id_].using_only_full_mkt_for_sim_):
                        new_size_ = self.dep_market_view_.ask_size(0)
                    else: 
                        new_size_ = self.dep_market_view_.market_update_info_.bestask_size_
                    if (self.sid_to_sim_config_[self.dep_security_id_].using_only_full_mkt_for_sim_):
                        new_ordercount_ = self.dep_market_view_.ask_order(0)
                    else: 
                        new_ordercount_ = self.dep_market_view_.market_update_info_.bestask_ordercount_
                    if (not self.dep_market_view_.trade_before_quote() and (not new_size_ == prev_size_ or order_.num_events_seen_ == 1)):
                        self.BackupQueueSizes(order_)
                    if (order_.num_events_seen_ == 0): # first time ... before this do not fill
                        order_.queue_size_behind_ = 0
                        if (self.sid_to_sim_config_[self.dep_security_id_].using_only_full_mkt_for_sim_):
                            order_.queue_size_ahead_ = self.dep_market_view_.ask_size(0)
                        else: 
                            order_.queue_size_ahead_ = self.dep_market_view_.market_update_info_.bestask_size_
                        order_.num_events_seen_ = 1
                    else: # not the first time
                        if (self.sid_to_sim_config_[self.dep_security_id_].use_tgt_sim_market_maker_):
                            self.UpdateQueueSizesTargetPrice(new_size_ , prev_size_, order_)
                        elif (self.sid_to_sim_config_[self.dep_security_id_].use_baseprice_tgt_sim_market_maker_):
                            self.UpdateQueueSizesBasePriceBasedTargetPrice(new_size_ , prev_size_, order_)
                        elif (self.sid_to_sim_config_[self.dep_security_id_].use_fgbm_sim_market_maker_):
                            self.UpdateQueueSizesTradeBased(new_size_, prev_size_, order_)
                        else:
                            self.UpdateQueueSizes(new_size_, prev_size_, order_)
            elif (self.sid_to_sim_config_[self.dep_security_id_].adjust_non_best_order_queues_):
                for order_ in order_vec_:
                    if (order_ is None):
                        continue
                    prev_size_ = order_.queue_size_behind_ + order_.queue_size_ahead_
                    if (self.sid_to_sim_config_[self.dep_security_id_].using_only_full_mkt_for_sim_):
                        new_size_ = self.dep_market_view_.ask_size(0)
                    else: 
                        new_size_ = self.dep_market_view_.market_update_info_.bestask_size_
                    if (not self.dep_market_view_.trade_before_quote() and (not new_size_ == prev_size_ or order_.num_events_seen_ == 1)):
                        self.BackupQueueSizes(order_)
                    if (order_.num_events_seen_ == 0): # first time ... before this do not fill
                        order_.queue_size_behind_ = 0
                        if (self.sid_to_sim_config_[self.dep_security_id_ ].using_only_full_mkt_for_sim_):
                            order_.queue_size_ahead_ = self.dep_market_view_.ask_size(0)
                        else: 
                            order_.queue_size_ahead_ = self.dep_market_view_.market_update_info_.bestask_size_
                        order_.num_events_seen_ = 1
                    else: # not the first time
                        if (self.sid_to_sim_config_[self.dep_security_id_].use_tgt_sim_market_maker_):
                            self.UpdateQueueSizesTargetPrice(new_size_ , prev_size_, order_)
                        elif (self.sid_to_sim_config_[self.dep_security_id_].use_baseprice_tgt_sim_market_maker_):
                            self.UpdateQueueSizesBasePriceBasedTargetPrice ( new_size_ , prev_size_, order_)
                        elif (self.sid_to_sim_config_[self.dep_security_id_].use_fgbm_sim_market_maker_):
                            self.UpdateQueueSizesTradeBased(new_size_, prev_size_, order_)
                        else:
                            self.UpdateQueueSizes(new_size_, prev_size_, order_)
            else:
                break
        
    def OnTradePrint(self, _trade_print_info_, _market_update_info_):
        return
        if (self.all_requests_):
            self.ProcessRequestQueue(True)
        t_trade_print_info_buysell_ = _trade_print_info_.buysell_
        if (t_trade_print_info_buysell_ == 'B'):
            askside_trade_size_ = _trade_print_info_.size_traded_
            if (self.masked_asks_):
                self.masked_asks_ = False
                if (self.bestask_int_price_ == _trade_print_info_.int_trade_price_):
                    for i in range(0, len(self.masked_from_market_data_asks_map_)):
                        self.masked_from_market_data_asks_map_[i] = max(self.masked_from_market_data_asks_map_[i] - _trade_print_info_.size_traded_, 0)
                        if (self.masked_from_market_data_asks_map_[i] > 0):
                            masked_asks_ = True
                else:
                    self.FillInValue(self.masked_from_market_data_asks_map_, 0)
    
            for price_ in self.intpx_to_ask_order_vec_.keys():
                if (price_ <= _trade_print_info_.int_trade_price_):
                    continue
                order_vec_ = self.intpx_to_ask_order_vec_[price_]
                if (price_ < _trade_print_info_.int_trade_price_):
                    # Limit Ask Order at a higher level than Lift Price (currently not checking masks ... simply filling)
                    if (order_vec_):
                        # non-zero orders at this price level
                        for order_ in order_vec_: # TODO: where is the watch_.tv condition?
                            this_size_executed_ = order_.ExecuteRemaining()
                            self.client_position_map_[order_.server_assigned_client_id()] -= this_size_executed_
                            self.global_position_to_send_map_[order_.server_assigned_client_id()] -= this_size_executed_
                            self.BroadcastExecNotification(order_.server_assigned_client_id(), order_)
                        order_vec_ = []
                else:
                    # Limit Ask Order at a same level/price than Lift trade in market (Check to see if executed, and Enqueue if not finished)
                    if (order_vec_):
                        # there are orders at this price level
                        # an estimate of the total_market_non_self_size at this level after this trade, we can use it to adjust queue_size_ahead_ and queue_size_behind_
                        if (self.dep_market_view_.market_update_info_.bestask_int_price_ > _trade_print_info_.int_trade_price_):
                            t_posttrade_asksize_at_trade_price_ = 0
                        else: 
                            t_posttrade_asksize_at_trade_price_ = self.dep_market_view_.market_update_info_.bestask_size_
                        for i in range(0, len(self.saci_to_executed_size_)):
                            self.saci_to_executed_size_[i] = 0
                        for order_ in order_vec_[:]:
                            # check which orders are executed, send message and deallocate order, nullify the pointer, erase from vector.
                            # Note the iterator does not need to be incremented since we either break out of loop or erase the iterator and hence increment it.
                            trd_size_ = _trade_print_info_.size_traded_
                            if (not self.dep_market_view_.trade_before_quote()):
                                trd_size_ = self.RestoreQueueSizes(order_, t_posttrade_asksize_at_trade_price_, trd_size_)
                            trade_size_to_be_used_ = _trade_print_info_.size_traded_ - self.saci_to_executed_size_[order_.server_assigned_client_id()]
                            if (trade_size_to_be_used_ <= 0):
                                continue
                            t_size_executed_ = order_.HandleCrossingTrade(trade_size_to_be_used_, t_posttrade_asksize_at_trade_price_)
                            if (t_size_executed_ > 0):
                                self.client_position_map_[order_.server_assigned_client_id()] -= t_size_executed_
                                self.global_position_to_send_map_[order_.server_assigned_client_id()] -= t_size_executed_
                                self.saci_to_executed_size_[order_.server_assigned_client_id()] += t_size_executed_
                                self.BroadcastExecNotification (order_.server_assigned_client_id(), order_)
                                if (order_.size_remaining() <= 0):
                                    order_vec_.remove(order_)
    
        if (t_trade_print_info_buysell_ == 'S'):
            # trade was a HIT, i.e. removing liquidity on the bid side
            bidside_trade_size_ = _trade_print_info_.size_traded_
            if (self.masked_bids_):
                self.masked_bids_ = False
                if (self.bestbid_int_price_ == _trade_print_info_.int_trade_price_):
                    for i in range(0, self.masked_from_market_data_bids_map_):
                        self.masked_from_market_data_bids_map_[i] = max(self.masked_from_market_data_bids_map_[i] - _trade_print_info_.size_traded_, 0)
                        if (self.masked_from_market_data_bids_map_[ i ] > 0):
                            self.masked_bids_ = True
                else:
                    self.FillInValue(self.masked_from_market_data_bids_map_, 0)
    
            for price_ in self.intpx_to_bid_order_vec_.keys():
                if (price_ < _trade_print_info_.int_trade_price_):
                    continue
                order_vec_ = self.intpx_to_bid_order_vec_[price_]
                if (price_ > _trade_print_info_.int_trade_price_):
                    # Aggressive Order at a lower level ( currently not checking masks ... simply filling )
                    if (order_vec_):
                        for order_ in order_vec_[:]:
                            this_size_executed_ = order_.ExecuteRemaining()
                            self.client_position_map_[order_.server_assigned_client_id()] += this_size_executed_
                            self.global_position_to_send_map_[order_.server_assigned_client_id()] += this_size_executed_
                            self.BroadcastExecNotification(order_.server_assigned_client_id(), order_)
                        order_vec_ = []
                else:
                    # ( i2bov_iter_->first == _trade_print_info_.int_trade_price_ ) ... trade at best-nonself-market. Check to see if executed, and Enqueue if not finished
                    if (order_vec_):
                        # an estimate of the total_market_non_self_size at this level after this trade, we can use it to adjust queue_size_ahead_ and queue_size_behind_
                        if (self.dep_market_view_.market_update_info_.bestbid_int_price_ < _trade_print_info_.int_trade_price_):
                            t_posttrade_bidsize_at_trade_price_ = 0
                        else: 
                            t_posttrade_bidsize_at_trade_price_ = self.dep_market_view_.market_update_info_.bestbid_size_
                        # an estimate of the total_market_non_self_size at this level after this trade, we can use it to adjust queue_size_ahead_ and queue_size_behind_    
                        for i in range(0, len(self.saci_to_executed_size_)):
                            self.saci_to_executed_size_[ i ] = 0
                        for order_ in order_vec_[:]:
                            # check which orders are executed, send message and deallocate order, nullify the pointer, erase from vector.
                            # Note the iterator does not need to be incremented since we either break out of loop or erase the iterator and hence increment it.
                            trade_size_to_be_used_ = _trade_print_info_.size_traded_ - self.saci_to_executed_size_[order_.server_assigned_client_id()]
                            if (trade_size_to_be_used_ <= 0):
                                continue
                            trd_size_ = _trade_print_info_.size_traded_
                            t_size_executed_ = order_.HandleCrossingTrade(trade_size_to_be_used_, t_posttrade_bidsize_at_trade_price_)
                            if (t_size_executed_ > 0):
                                self.client_position_map_ [order_.server_assigned_client_id ( ) ] += t_size_executed_
                                self.global_position_to_send_map_ [order_.server_assigned_client_id ( ) ] += t_size_executed_
                                self.saci_to_executed_size_[order_.server_assigned_client_id ( ) ] += t_size_executed_
                                self.BroadcastExecNotification(order_.server_assigned_client_id ( ), order_)
                                if (order_.size_remaining() <= 0):
                                    order_vec_.remove(order_)
    
    def OnTimePeriodUpdate(self, num_pages_to_add_):
        if len(self.all_requests) > 0 :
            self.ProcessRequestQueue(False) 
            
            '''False is needed ao that cancel req will not be removed '''
'''         
    def BroadcastConfirm(self):
        
    def BroadcastCancelNotification(self):
        
    def BroadcastExecNotification(self):
        
    def BroadcastOrderNone(self):
        
        
    def CxlOrdersAboveBestLevel(self):
        
    def UpdateQueueSizes(self):
        
    def UpdateQueueSizesTradeBased(self):
        
    def UpdateQueueSizesTargetPrice(self):
        
    def UpdateQueueSizesBasePriceBasedTargetPrice(self):
        
    def MatchTradeAndQuote(self):
        
        
    def SubscribeL2Events(self):
        
    def OnTimePeriodUpdade(self):
        
    def OnMarketUpdate(self):
        
    def OnTradePrint(self):
        
    def OrderNotFound(self):
        
    def OrderSequenced(self):
        
    def OrderSequencedAtTime(self):
        
    def OrderConfirmed(self):
        
    def OrderConfirmedAtTime(self):
        
    def OrderORSConfirmed(self):
        
    def OrderConfCxlReplaced(self):

    def OrderCanceled(self):

    def OrderCanceledAtTime(self):

    def OrderCxlSequencedAtTime(self):
        
    def OrderCancelRejected(self):
        
    def OrderExecuted(self):
        '''