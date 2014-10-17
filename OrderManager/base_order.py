class BaseOrder:
    
    def __init__(self):
        self.security_name_ = ''
        self.buysell_ = 0
        self.price_ = 0
        self.size_remaining_ = 0
        self.size_executed_ = 0
        self.size_requested_ = 0
        self.int_price_ = 0
        self.order_status_ = 0 # List out the possible values
        
        self.queue_size_ahead_ = 0
        self.queue_size_behind_ = 0
        
        self.client_assigned_order_sequence_ = 0
        
        # Might be useless
        self.seqd_msec_ = 0
        self.conf_msec_ = 0
        
        self.canceled_ = False
        self.replayed_ = False
        
    def security_name(self):
        return self.security_name_
    
    def buy_sell(self):
        return self.buysell_
    
    def price(self):
        return self.price_
    
    def size_remaining(self):
        return self.size_remaining_
    
    def size_executed(self):
        return self.size_executed_
    
    def size_requested(self):
        return self.size_requested_
    
    def int_price(self):
        return self.int_price_
    
    def order_status(self):
        return self.order_status_
    
    # Might be useless, check
    def cancelled(self):
        return self.canceled_
    
    def replayed(self):
        return self.replayed_
    
    def execute_remaining(self):
        t_size_remaining_ = self.size_remaining_
        self.size_remaining_ = 0
        self.size_executed_ += t_size_remaining_
        return t_size_remaining_