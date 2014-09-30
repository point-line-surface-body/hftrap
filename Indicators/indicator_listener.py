

class IndicatorListener():
    def OnIndicatorUpdate(self, indicator_index, new_value):
        return
    def __eq__(self, indicator_listener):
        return self.indicator_index == indicator_listener.indicator_index
    

class IndicatorListenerPair():
    
    def __init__(self, indicator_index, indicator_listener, node_value):
        self.indicator_index = indicator_index
        self.indicator_listener = indicator_listener
        self.node_value = node_value
        
    def __eq__(self, indicator_listener_pair):
        return self.indicator_index == indicator_listener_pair.indicator_index and self.indicator_listener == indicator_listener_pair.indicator_listener and self.node_value == indicator_listener_pair.node_value 
        
    def OnIndicatorUpdate(self, indicator_value):
        self.indicator_listener.OnIndicatorUpdate(self.indicator_index,indicator_value*self.node_value )
        
        
class UnweightedIndicatorListenerPair():
    def __init__(self,  indicator_index, indicator_listener):
        self.indicator_index_ = indicator_index
        self.indicator_listener__ = indicator_listener
        
    def __eq__(self, unweighted_listener_pair):
        return self.indicator_index_ == unweighted_listener_pair.indicator_index_ and self.indicator_listener == unweighted_listener_pair.indicator_listener
    
    def OnIndicatorUpdate(self, indicator_value):
        self.indicator_listener.OnIndicatorUpdate(self.indicator_index,indicator_value)
        
        