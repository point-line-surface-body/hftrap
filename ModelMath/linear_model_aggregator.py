from ModelMath.base_model_math import BaseModelMath

class LinearModelAggregator(BaseModelMath):
    
    def __init__(self, _watch_, _model_filename_, _dep_market_view_, _base_pricetype_):
        super(LinearModelAggregator, self).__init__(_watch_, _model_filename_)
        self.dep_market_view_ = _dep_market_view_
        self.dep_baseprice_type_ = _base_pricetype_
        self.sum_vars_ = 0
        self.last_propagated_target_price_ = 0
        self.model_intercept_ = 0
        self.count_ = 0
        
    def SetBasePrice(self):
        for t_indicator_ in self.indicator_vec_:
            t_indicator_.SetBasepxPxtype(self.dep_market_view_, self.dep_baseprice_type_)
        
    def FinishCreation(self):
        if (not self.is_ready_vec_):
            self.is_ready_ = True
    
    def AreAllReady(self):
        if (not self.dep_market_view_.is_ready_):
            return False
        # Implied price, mid price condition, not used
        for i in range(0, len(self.is_ready_vec_)):
            if (not self.is_ready_vec_[i] and self.readiness_required_vec_[i]):
                return False
        return True
            
    def OnIndicatorUpdate(self, _indicator_index_, _new_value_):
        self.count_ += 1
        print('LMA.OnIndicatorUpdate: '+str(self.count_)+' '+str(_indicator_index_)+' '+str(_new_value_))
        #print(len(self.prev_value_vec_))
        if (not self.is_ready_):
            self.is_ready_vec_[_indicator_index_] = True
            self.is_ready_ = self.AreAllReady()
            if (not self.is_ready_):
                # Some indicator is not ready but at least one other is ready
                for i in range(0, len(self.indicator_vec_)):
                    if (not self.is_ready_vec_[i]):
                        # This indicator is not ready
                        if (self.indicator_vec_[i].IsIndicatorReady()):
                            self.is_ready_vec_[i] = True
                            self.is_ready_ = self.AreAllReady()
                        else:
                            print 'Indicator Not Ready '+str(i)+' '+self.indicator_vec_[i].ConciseIndicatorDescription()
                            self.indicator_vec_[i].WhyNotReady()
            if (self.is_ready_):
                self.last_is_ready_ = True
        else:
            # Check for nan value in _new_value_
            #print('indicator_index: '+str(_indicator_index_))
            #print(str(_new_value_)+' '+str(self.prev_value_vec_[_indicator_index_]))
            if (abs(_new_value_-self.prev_value_vec_[_indicator_index_]) > 10*self.dep_market_view_.MinPriceIncrement()):
                print 'HUGE value in sum_vars'
            self.sum_vars_ += (_new_value_-self.prev_value_vec_[_indicator_index_])
            self.prev_value_vec_[_indicator_index_] = _new_value_
    
    # What?
    def MultiplyIndicatorNodeValuesBy(self, _mult_factor_):
        for i in range(0, len(self.indicator_vec_)):
            self.indicator_vec_[i].MultiplyIndicatorListenerWeight(self, _mult_factor_)
        self.sum_vars_ += (_mult_factor_-1)*self.model_intercept_
        self.model_intercept_ *= _mult_factor_
        
    def ShowIndicatorValues(self):
        for i in range(0, len(self.indicator_vec_)):
            print ' value: '+self.prev_value_vec_[i]/self.dep_market_view_.min_price_increment() + ' of '+self.indicator_vec_[i].ConciseIndicatorDescription() 

    def SMVOnReady(self):
        self.CalcAndPropagate()
            
    def CalcAndPropagate(self):
        #print('*******************************'+str(self.is_ready_)+'*******************************')
        if (self.is_ready_):
            print 'LMA.CalcAndPropagate: '+str(self.count_)
            t_new_target_bias = self.sum_vars_
            t_new_target_price = self.dep_market_view_.GetPriceFromType(self.dep_baseprice_type_) + t_new_target_bias
            
            kMinTicksMoved = 0.015
            if ((t_new_target_price - self.last_propagated_target_price_) > kMinTicksMoved*self.dep_market_view_.MinPriceIncrement()):
                self.PropagateNewTargetPrice(t_new_target_price, t_new_target_bias)
                self.last_propagated_target_price_ = t_new_target_price
        else:
            if (self.last_is_ready_):
                self.PropagateNotReady();
                self.last_is_ready_ = False