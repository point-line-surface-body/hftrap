from struct import unpack

class Message:
    
    def __init__(self, _bytes_):
        attributes_ = unpack('fcHHHHHH', _bytes_)
        self.timestamp_ = attributes_[0]
        self.type_ = attributes_[1]
        self.bid_orders_ = attributes_[2]
        self.bid_size_ = attributes_[3]
        self.bid_price_ = attributes_[4]
        self.ask_price_ = attributes_[5]
        self.ask_size_ = attributes_[6]
        self.ask_orders_ = attributes_[7]
        
    def __del__(self):
        return