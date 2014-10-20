class IndicatorListener():
    
    def OnIndicatorUpdate(self, _indicator_index_, _new_value_):
        return
    
    def __eq__(self, _indicator_listener_):
        return self.indicator_index_ == _indicator_listener_.indicator_index_
    
class IndicatorListenerPair():
    
    def __init__(self, _indicator_index_, _indicator_listener_, _node_value_):
        self.indicator_index_ = _indicator_index_
        self.indicator_listener_ = _indicator_listener_
        self.node_value_ = _node_value_
        
    def __eq__(self, _indicator_listener_pair_):
        return self.indicator_index_ == _indicator_listener_pair_.indicator_index_ and self.indicator_listener_ == _indicator_listener_pair_.indicator_listener_ and self.node_value_ == _indicator_listener_pair_.node_value_
        
    def OnIndicatorUpdate(self, _indicator_value_):
        self.indicator_listener_.OnIndicatorUpdate(self.indicator_index_, _indicator_value_ * self.node_value_)
        
# class UnweightedIndicatorListenerPair():
#     def __init__(self,  indicator_index, indicator_listener):
#         self.indicator_index_ = indicator_index
#         self.indicator_listener__ = indicator_listener
#         
#     def __eq__(self, unweighted_listener_pair):
#         return self.indicator_index_ == unweighted_listener_pair.indicator_index_ and self.indicator_listener == unweighted_listener_pair.indicator_listener
#     
#     def OnIndicatorUpdate(self, indicator_value):
#         self.indicator_listener.OnIndicatorUpdate(self.indicator_index,indicator_value)