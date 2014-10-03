class BaseOrder:
    
    def __init__(self):
        self.security_name = ''
        self.buy_sell = 0 # 1 represents BUY, 2 represents SELL
        self.price = 0
        self.size_remaining = 0
        self.size_executed = 0
        self.size_requested = 0
        self.int_price = 0
        self.order_status = 0 # List out the possible values
        
        self.queue_size_ahead = 0
        self.queue_size_behind = 0
        
        self.client_assigned_order_sequence = 0
        
        # Might be useless
        self.seqd_msec = 0
        self.conf_msec = 0
        
        self.cancelled = False
        self.replayed = False
        
    def security_name(self):
        return self.security_name
    
    def buy_sell(self):
        return self.buy_sell
    
    def price(self):
        return self.price
    
    def size_remaining(self):
        return self.size_remaining
    
    def size_executed(self):
        return self.size_executed
    
    def size_requested(self):
        return self.size_requested
    
    def int_price(self):
        return self.int_price
    
    def order_status(self):
        return self.order_status
    
    # Might be useless
    def cancelled(self):
        return self.cancelled
    
    def replayed(self):
        return self.replayed