class ContractSpecification(object):
    def __init__(self, *argv):
        self.min_price_increment_ = 1.0
        self.numbers_to_dollars_ = 1.0
        self.exch_source_ = "INVALID"
        self.min_order_size_ = 1
        if len(argv) == 3 :
            self.min_price_increment_ = (float)(argv[0])
            self.numbers_to_dollars_ = (float)(argv[1])
            self.min_order_size_ = (int)(argv[2])
            
class SecurityDefinitions(object):
    contract_specification_map_ = {}
    
    def __init__ (self, trading_date_):
        self.trading_date_ = trading_date_
        if "ZN_0" not in SecurityDefinitions.contract_specification_map_.keys() :
            SecurityDefinitions.contract_specification_map_["ZN_0"] = ContractSpecification(0.015625, 1000, 1)
        if "ZB_0" not in SecurityDefinitions.contract_specification_map_.keys() :
            SecurityDefinitions.contract_specification_map_["ZB_0"] = ContractSpecification(0.031250, 1000, 1)
    
    @staticmethod
    def GetContractMinPriceIncrement(_shortcode_, *argv):
        if (_shortcode_ == 'ZN_0' or _shortcode_ == 'ZN_1'):
            return 0.015625
        elif (_shortcode_ == 'ZB_0'):
            return 0.031250
        else:
            return 0