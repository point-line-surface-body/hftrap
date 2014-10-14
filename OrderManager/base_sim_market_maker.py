from OrderManager.base_order import BaseOrder
class BaseSimMarketMaker:
    
    '''constructor'''
    def __init__(self):
        self.all_requests = []
        self.pending_requests = []
        self.all_requests_lock = False
        return
    
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
        if (self.all_requests_lock):
            self.pending_requests.append(_request_)
        else:
            self.all_requests.append(_request_)
            self.all_requests.sort() #stable_sort(self.all_requests) # Corrected this)
    
    def ProcessRequestQueue(self): # Later find out whether that boolean variable is needed
        if (self.all_requests_lock):
            return
        self.all_requests_lock = True
        for request in self.all_requests:
            if (request.wakeup_time > self.watch.tv()):
                continue
            if (request.request_type == ORQ_SEND):
                order = request.order
                # This order will always get confirmed
                order.Confirm()
                # Broadcast this information
                if (order.buy_sell == 1): # Buy
                    
                    # Bid side order         
                    # Update queue sizes
                    order.queue_size_behind = 0
                    order.queue_size_ahead = self.dep_market_view.bid_size_at_int_price(order.int_price)
                    
                    # Check if aggressive
                    if (order.int_price >= self.dep_market_view.best_ask_int_price()):
                        # Reset to the best ask level
                        order.int_price = self.dep_market_view.best_ask_int_price()
                        order.price = self.dep_market_view.best_ask_price()
                        
                        # Execute the order, update position, send Exec
                        if (self.dep_market_view.bestask_size()-self.masked_from_market_data_asks_map[order.server_assigned_client_id] > 0):
                            if ((self.dep_market_view.bestask_size()-self.masked_from_market_data_asks_map[order.server_assigned_client_id]) >= order.size_remaining()):
                                # Full execution
                                size_executed = order.ExecuteRemaining()
                                self.client_position_map[server_assigned_client_id] += size_executed
                                self.global_position_to_send_map[server_assigned_client_id] += size_executed

                                # BroadcastExecNotification ( r_server_assigned_client_id_, p_new_sim_order_ ) ;
                                self.masked_from_market_data_asks_map[server_assigned_client_id] += size_executed
                                self.masked_asks = True
                            else:
                                # Partial execution
                                size_executed = order.MatchPartial(self.dep_market_view.bestask_size()-self.masked_from_market_data_asks_map[server_assigned_client_id])
                                self.client_position_map[server_assigned_client_id] += size_executed
                                self.global_position_to_send_map[server_assigned_client_id] += size_executed

                                # BroadcastExecNotification ( r_server_assigned_client_id_, p_new_sim_order_ ) ;
                                self.masked_from_market_data_asks_map[server_assigned_client_id] += size_executed
                                self.masked_asks = True

                                self.int_price_to_bid_order_vec[order.int_price].append(order)
                                if (order.int_price > self.dep_market_view_.bestbid_int_price()):
                                    order.alone_above_best_market_ = True
                    else:
                        # Add liquidity order
                        self.int_price_to_bid_order_vec[order.int_price].append(order)
                        if (order.int_price > self.dep_market_view.bestbid_int_price()):
                            order.alone_above_best_market = True
                else:
                    
                    # Ask side order
                    # Update queue sizes
                    order.queue_size_behind = 0
                    order.queue_size_ahead = self.dep_market_view.ask_size_at_int_price(order.int_price)
                    
                    # Check if aggressive
                    if (order.int_price <= self.dep_market_view.bestbid_int_price()):
                        # Reset to the best ask level
                        order.int_price = self.dep_market_view.bestbid_int_price()
                        order.price = self.dep_market_view.bestbid_price()
                        
                        # Execute the order, update position, send Exec
                        if (self.dep_market_view.bestbid_size()-self.masked_from_market_data_bids_map[order.server_assigned_client_id] > 0):
                            if ((self.dep_market_view.bestbid_size()-self.masked_from_market_data_bids_map[order.server_assigned_client_id]) >= order.size_remaining()):
                                # Full execution
                                size_executed = order.ExecuteRemaining()
                                self.client_position_map[server_assigned_client_id] += size_executed
                                self.global_position_to_send_map[server_assigned_client_id] += size_executed

                                # BroadcastExecNotification ( r_server_assigned_client_id_, p_new_sim_order_ ) ;
                                self.masked_from_market_data_bids_map[server_assigned_client_id] += size_executed
                                self.masked_asks = True
                            else:
                                # Partial execution
                                size_executed = order.MatchPartial(self.dep_market_view.bestbid_size()-self.masked_from_market_data_asks_map[server_assigned_client_id])
                                self.client_position_map[server_assigned_client_id] += size_executed
                                self.global_position_to_send_map[server_assigned_client_id] += size_executed

                                # BroadcastExecNotification ( r_server_assigned_client_id_, p_new_sim_order_ ) ;
                                self.masked_from_market_data_bids_map[server_assigned_client_id] += size_executed
                                self.masked_asks = True

                                self.int_price_to_ask_order_vec[order.int_price].append(order)
                                if (order.int_price > self.dep_market_view_.bestask_int_price()):
                                    order.alone_above_best_market_ = True
                    else:
                        # Add liquidity order
                        self.int_price_to_ask_order_vec[order.int_price].append(order)
                        if (order.int_price > self.dep_market_view.bestask_int_price()):
                            order.alone_above_best_market = True
                            
            elif (request.request_type == ORQ_CANCEL):
                if (self.process_only_sendtrades):
                    return
                to_postpone = 0
                server_assigned_order_sequence = request.sreq_.scor_.server_assigned_order_sequence_
                buysell = request.sreq_.scor_.buysell
                int_price = request.sreq_.scor_.int_price_

                order = self.FetchOrder(buysell, int_price, server_assigned_order_sequence)

                # Probably only the first condition is required
                if (order is not None and (order.server_assigned_client_id == server_assigned_client_id)):
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
                                else
                                    if (self.dep_market_view.SpreadWiderThanNormal()):
                                        to_postpone = 3
                        if (order.IsExecuted()):
                            # Prematurely executed, just waiting on the OnTradePrint call.
                            to_postpone = 4
                        if (to_postpone == 0):
                            UniqueVectorRemove(self.int_price_to_bid_order_vec[order.int_price], order)
                            BroadcastCancelNotification(r_server_assigned_client_id, order)
                        else:
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
                            UniqueVectorRemove (int_price_to_ask_order_vec[order.int_price], order)
                            BroadcastCancelNotification(r_server_assigned_client_id_, order)
        
        if (self.pending_requests):
            for request in self.pending_requests:
                self.all_requests.append(request)
            self.pending_request = []
        self.all_requests_lock = False    
    
    def SendOrderExch(self, _client_id_, _security_name_, _buy_sell_, _price_, _size_requested_, _int_price_, _order_sequence_):
        new_order = BaseOrder()
        new_order.security_name = _security_name_
        new_order.buy_sell = _buy_sell_
        new_order.price = _price_
        new_order.size_remaining = _size_requested_
        new_order.int_price = _int_price_
        new_order.order_status = 0 # Not Needed
        
        new_order.queue_size_ahead = 0
        new_order.queue_size_behind = 0
        
        # new_order.num_events_seen = 0
        new_order.client_assigned_order_sequence = _order_sequence_
        new_order.server_assigned_order_sequence = 
        
        new_order.seqd_msec = self.watch.tv()
        
        # Size requested must be a multiple of MinOrderSize
        if (_size_requested_ mod self.dep_market_view.min_order_size() != 0):
            # Broadcast rejection
            
        # Broadcast sequenced
        
        # Create a request class
        
        # Wrap new_order in a request object
        
        new_request = Request()
        AddRequest(new_request)
    
    def CancelOrderExch(self):
        