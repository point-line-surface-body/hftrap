from OrderManager.base_order import BaseOrder
from MarketAdapter.security_market_view_change_listener import SecurityMarketViewChangeListener
from ExternalData.external_time_listener import TimePeriodListener
from OrderManager.request import Request
        

class BaseSimMarketMaker(SecurityMarketViewChangeListener, TimePeriodListener):
    
    shcToSMMmap = dict()

    '''constructor'''
    def __init__(self, watch, smv):
        self.watch_ = watch
        self.all_requests = []
        self.pending_requests = []
        self.all_requests_lock = False
        
        self.dep_market_view_ = smv
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
        self.dep_market_view_.subscribe_price_type(self, "MktSizeWPrice")
        self.watch_.subscribe_BigTimePeriod(self) # may make small Time period also in watch
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
    def ProcessRequestQueue(self): # Later find out whether that boolean variable is needed
        if (self.all_requests_lock_):
            return
        self.all_requests_lock = True
        for request in self.all_requests:
            server_assigned_client_id = request.server_assigned_client_id_
            if (request.wakeup_time > self.watch.tv()):
                continue
            if (request.request_type == "SEND"):
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
                            
            elif (request.request_type == "CANCEL"):
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
        
        if (self.pending_requests):
            for request in self.pending_requests:
                self.all_requests.append(request)
            self.pending_request = []
        self.all_requests_lock = False    
    
    def SendOrderExch(self, _server_assigned_client_id_, _security_name_, _buysell_, _price_, _size_requested_, _int_price_, _client_assigned_order_sequence_):
        order_ = BaseOrder()
        order_.security_name_ = _security_name_
        order_.buysell_ = _buysell_
        order_.price_ = _price_
        order_.size_remaining_ = _size_requested_
        order_.int_price_ = _int_price_
        order_.order_status_ = 0 # Not Needed
        
        order_.queue_size_ahead_ = 0
        order_.queue_size_behind_ = 0
        
        order_.num_events_seen_ = 0
        order_.client_assigned_order_sequence_ = _client_assigned_order_sequence_
        order_.server_assigned_order_sequence_ = self.server_assigned_order_sequence_
        self.server_assigned_order_sequence_ += 1
        
        order_.server_assigned_client_id_ = self.servr
        
        order_.order_sequenced_time_ = self.watch.tv()
        
        # Size requested must be a multiple of MinOrderSize
        if (not _size_requested_ % self.dep_market_view.min_order_size() != 0):
            # Broadcast rejection
            self.BroadcastRejection(_server_assigned_client_id_, order_, 'kSendOrderRejectNotMinOrderMultiple')
            
        self.saos_to_seqd_time_[order_.server_assigned_order_sequence_] = self.watch_.tv()
        # Broadcast sequenced
        self.BroadcastSequenced(_server_assigned_client_id_, order_)
        
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
            
    def OnMarketUpdate(self, _security_id_, _market_update_info_):
        old_bestbid_int_price_ = self.bestbid_int_price_
        old_bestbid_size_ = self.bestbid_size_
        old_bestask_int_price_ = self.bestask_int_price_
        old_bestask_size_ = self.bestask_size_
        if self.bestbid_size_ < _market_update_info_.bestbid_size_ :
            self.last_bid_size_change_msecs_ = self.watch_.GetMsecsFromMidnight()
        if self.bestask_size_ < _market_update_info_.bestask_size_  :
            self.last_ask_size_change_msecs_ = self.watch_.GetMsecsFromMidnight()
        if old_bestask_int_price_ > _market_update_info_.bestask_int_price_ :
            if self.dep_market_view_.market_update_info_.asklevels_[0].limit_ordercount_ ==1:
                self.ask_side_priority_order_exists_ = True
                self.ask_side_priority_order_size_ = self.dep_market_view_.market_update_info_.asklevels_[0].limit_size_
            else:
                self.ask_side_priority_order_exists_ = False
                self.ask_side_priority_order_size_ = 0
        if old_bestbid_int_price_ < _market_update_info_.bestbid_int_price_ :
            if self.dep_market_view_.market_update_info_.bidlevels_[0].limit_ordercount_ ==1 :
                self.bid_side_priority_order_exists_ = True
                self.bid_side_priority_order_size_ = self.dep_market_view_.market_update_info_.bidlevels_[0].limit_size_
            else :
                self.bid_side_priority_order_exists_ = False
                self.bid_side_priority_order_size_ = 0
        
    def OnTradePrint(self, _security_id_, _trade_print_info_, _market_update_info_):
        if (self.all_requests_):
            self.ProcessRequestQueue(True)
        if (_trade_print_info_.buysell_ == 'Buy'):
            for price_ in self.intpx_to_ask_order_vec_:
                pass
        elif (_trade_print_info_.buysell_ == 'Sell'):
            pass
        return
    
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