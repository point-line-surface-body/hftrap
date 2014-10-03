from ModelMath.base_model_math import BaseModelMath

class LinearModelAggregator(BaseModelMath):
    
    def __init__(self, _watch_, _model_filename_, _dep_market_view_, _dep_base_price_type_):
        super(LinearModelAggregator, self).__init__(_watch_, _model_filename_)
        self.dep_market_view = _dep_market_view_
        self.prev_value_vec = []
        self.sum_vars = 0
        self.last_propagated_target_price = 0
        self.model_intercept = 0
    
    def AreAllReady(self):
        if (not self.dep_market_view.is_ready()):
            return False
        # Implied price, mid price condition, not used
        for i in range(0, len(self.is_ready_vec)):
            if (not self.is_ready_vec[i] and self.readiness_required_vec[i]):
                return False
        return True
            
    def OnIndicatorUpdate(self, _indicator_index_, _new_value_):
        if (not self.is_ready):
            self.is_ready_vec[_indicator_index_] = True
            self.is_ready = self.AreAllReady()
            if (not self.is_ready):
                # Some indicator is not ready but at least one other is ready
                for i in range(0, len(self.indicator_vec)):
                    if (not self.is_ready_vec[i]):
                        # This indicator is not ready
                        if (self.indicator_vec[i].IsIndicatorReady()):
                            self.is_ready_vec[i] = True
                            self.is_ready = self.AreAllReady()
                        else:
                            print 'Indicator Not Ready '+str(i)+' '+self.indicator_vec[i].ConciseIndicatorDescription()
                            self.indicator_vec[i].WhyNotReady()
            if (self.is_ready):
                self.last_is_ready = True
        else:
            # Check for nan value in _new_value_
            if (abs(_new_value_-self.prev_value_vec[_indicator_index_]) > 10*self.dep_market_view.min_price_increment()):
                print 'HUGE value in sum_vars'
            self.sum_vars += (_new_value_-self.prev_value_vec[_indicator_index_])
            self.prev_value_vec[_indicator_index_] = _new_value_
    
    # What?
    def MultiplyIndicatorNodeValuesBy(self, _mult_factor_):
        for i in range(0, len(self.indicator_vec)):
            self.indicator_vec[i].MultiplyIndicatorListenerWeight(self, _mult_factor_)
        self.sum_vars += (_mult_factor_-1)*self.model_intercept
        self.model_intercept *= _mult_factor_
        
    def ShowIndicatorValues(self):
        for i in range(0, len(self.indicator_vec)):
            print ' value: '+self.prev_value_vec[i]/self.dep_market_view.min_price_increment()
                + ' of '+self.indicator_vec[i].ConciseIndicatorDescription()
        
    def CalcAndPropagate(self):
        if (self.is_ready):
            t_new_target_bias = self.sum_vars
            t_new_target_price = something
            
            kMinTicksMoved = 0.015
            if ((t_new_target_price - self.last_propagated_target_price) > kMinTicksMoved*self.dep_market_view.min_price_increment()):
                self.PropagateNewTargetPrice(t_new_target_price, t_new_target_bias)
                self.last_propagated_target_price = t_new_target_price
        else:
            if (self.last_is_ready):
                self.PropagateNotReady();
                self.last_is_ready = False