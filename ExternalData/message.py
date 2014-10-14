from struct import unpack

class Message:
    
    def __init__(self, _bytes_):
        attributes = unpack('fcHHHHHH', _bytes_)
        self.timestamp = attributes[0]
        self.type = attributes[1]
        self.bid_orders = attributes[2]
        self.bid_size = attributes[3]
        self.bid_price = attributes[4]
        self.ask_price = attributes[5]
        self.ask_size = attributes[6]
        self.ask_orders = attributes[7]
        
    def __del__(self):
        return