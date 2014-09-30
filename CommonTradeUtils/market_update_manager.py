from MarketAdapter.security_market_view_change_listener import SecurityMarketViewChangeListener
from ExternalData.external_time_listener import TimePeriodListener


class MarketUpdateManager(TimePeriodListener, SecurityMarketViewChangeListener):
    
    def __init__(self):
        return