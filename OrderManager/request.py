from OrderManager.base_order import BaseOrder

class Request:
    def __init__(self):
        self.wakeup_time_ = 0
        self.request_type_ = None #"CANCEL", "SEND" , "REPLACE"
        self.order_ = BaseOrder()
        self.server_assigned_client_id_ = 0
        self.server_assigned_order_sequence_ = 0
        self.postpone_once_ = False # do we need this ?