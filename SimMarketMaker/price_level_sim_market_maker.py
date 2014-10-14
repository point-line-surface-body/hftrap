from MarketAdapter.security_market_view_change_listener import SecurityMarketViewChangeListener
from ExternalData.external_time_listener import TimePeriodListener

class PriceLevelSimMarketMaker(SecurityMarketViewChangeListener,TimePeriodListener):
    
    def __init__(self, watch_, smv):
        return 