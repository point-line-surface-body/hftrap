class BaseTrader():
    
    def __init__(self, _base_sim_market_maker_):
        self.base_sim_market_maker_ = _base_sim_market_maker_
        self.client_id_ = self.base_sim_market_maker_.Connect()
        
    def SendTrade(self, _order_):
        self.base_sim_market_maker_.SendOrderExch(self.client_id_, _order_.security_name(), _order_.buysell(), _order_.price(), _order_.size_requested(), _order_.int_price(), _order_.client_assigned_order_sequence())
        
    def Cancel (self, _order_):
        self.base_sim_market_maker_.CancelOrderExch(self.client_id_,_order_.server_assigned_order_sequence(), _order_.buysell(), _order_.int_price())
    
    def Modify(self, _order_, _new_size_requested_):
        self.base_sim_market_maker_.CancelReplaceOrderExch(self.client_id_,_order_.server_assigned_order_sequence(), _order_.buysell(), _order_.int_price(), _new_size_requested_)
        
    def Replay(self, _order_):
        self.base_sim_market_maker_.ReplayOrderExch(self.client_id_, _order_.client_assigned_order_sequence(), _order_.buysell(), _order_.int_price(), _order_.server_assigned_order_sequence())
        
    def GetClientId(self):
        return self.client_id_