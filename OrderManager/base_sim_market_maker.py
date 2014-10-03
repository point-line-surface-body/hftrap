from OrderManager.base_order import BaseOrder
class BaseSimMarketMaker:
    
    def __init__(self):
        self.all_requests = []
        self.pending_requests = []
        self.all_requests_lock = False
        return
    
    def AddRequest(self, _request_):
        if (self.all_requests_lock):
            self.pending_requests.append(_request_)
        else:
            self.all_requests.append(_request_)
            stable_sort(self.all_requests) # Correct this
    
    def ProcessRequestQueue(self): # Later find out whether that boolean variable is needed
        if (self.all_requests_lock):
            return
        self.all_requests_lock = True
        
        
        
        
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
        