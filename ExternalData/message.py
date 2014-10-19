from struct import unpack

class Message:
    
    def __init__(self, _bytes_):
        attributes_ = unpack('QIccHHHHHHHH', _bytes_)
        self.sec_ = attributes_[0]
        self.usec_ = attributes_[1]
        self.type_ = attributes_[2]
        self.buysell_ = attributes_[3]
        self.bid_orders_ = attributes_[4]
        self.bid_size_ = attributes_[5]
        self.bid_price_ = attributes_[6]
        self.ask_price_ = attributes_[7]
        self.ask_size_ = attributes_[8]
        self.ask_orders_ = attributes_[9]
        self.trade_size_ = attributes_[10]
        self.trade_price_ = attributes_[11]
        self.timestamp_ = (self.sec_ * 1000 + self.usec_ / 1000) % 86400000
        
    def Dump(self):
        print('-------------------------------')
        print('sec_:\t\t'+str(self.sec_))
        print('usec_:\t\t'+str(self.usec_))
        print('type_:\t\t'+str(self.type_))
        print('buysell_:\t'+str(self.buysell_))
        print('bid_orders_:\t'+str(self.bid_orders_))
        print('bid_size_:\t'+str(self.bid_size_))
        print('bid_price_:\t'+str(self.bid_price_))
        print('ask_orders_:\t'+str(self.ask_orders_))
        print('ask_size_:\t'+str(self.ask_size_))
        print('ask_price_:\t'+str(self.ask_price_))
        print('trade_size_:\t'+str(self.trade_size_))
        print('trade_price_:\t'+str(self.trade_price_))
        print('timestamp_:\t'+str(self.timestamp_))
        print('--------------------------------')