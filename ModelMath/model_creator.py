from ModelMath.linear_model_aggregator import LinearModelAggregator
from Indicators.simple_trend import SimpleTrend

class ModelCreator():
    
    def __init__(self):
        return
    
    @staticmethod
    def CollectShortCodesFromIndicator(_tokens_, _source_shortcode_vec_):
        if (_tokens_[2] == 'SimpleTrend'):
            SimpleTrend.CollectShortCodes(_source_shortcode_vec_, _tokens_)
    
    @staticmethod
    def CollectShortCodes(_model_filename_, _source_shortcode_vec_):
        print('ModelCreator.CollectShortCodes')
        t_model_file_ = open(_model_filename_, 'r')
        t_current_phase_ = 0
        while (1):
            t_line_ = t_model_file_.readline()
            if (t_line_ is None or t_line_ == ''):
                break
            t_tokens_ = t_line_.split()
            if (t_current_phase_ == 0):
                if (len(t_tokens_) < 5):
                    print 'ModelFile Incorrect'
                    exit()
                assert t_tokens_[0] == 'MODELINIT'
                assert t_tokens_[1] == 'DEPBASE'
                t_current_phase_ = 1
            elif (t_current_phase_ == 1):
                if (len(t_tokens_) < 3):
                    print 'ModelFile Incorrect'
                    exit()
                assert t_tokens_[0] == 'MODELMATH'
                assert t_tokens_[1] == 'LINEAR'
                assert t_tokens_[2] == 'CHANGE'
                t_current_phase_ = 2
            elif (t_current_phase_ == 2):
                if (len(t_tokens_) < 1):
                    print 'ModelFile Incorrect'
                assert t_tokens_[0] == 'INDICATORSTART'
                t_current_phase_ = 3
            elif (t_current_phase_ == 3):
                if (len(t_tokens_) < 1):
                    print 'ModelFile Incorrect'
                    exit()
                assert t_tokens_ == 'INDICATOR' or 'INDICATOREND'
                if (t_tokens_[0] == 'INDICATOR'):
                    if (len(t_tokens_) < 3):
                        print 'ModelFile Incorrect'
                        exit()
                    ModelCreator.CollectShortCodesFromIndicator(t_tokens_, _source_shortcode_vec_)
                else:
                    t_current_phase_ = 4
            elif (t_current_phase_ == 4):
                break
                
    
    @staticmethod
    def GetIndicatorFromTokens(_watch_, _tokens_, _dep_base_pricetype_):
        '''Add more later''' 
        if (_tokens_[2] == 'SimpleTrend'):
            return SimpleTrend.GetUniqueInstance(_watch_, _tokens_, _dep_base_pricetype_)
    
    @staticmethod
    def CreateModelMathComponent(_watch_, _model_filename_):
        print('ModelCreator.CreateModelMathComponent')
        t_model_file_ = open(_model_filename_, 'r')
        t_current_phase_ = 0
        t_dep_shortcode_ = None
        t_dep_base_pricetype_ = None
        t_model_math_ = None
        while (1):
            t_line_ = t_model_file_.readline()
            if (t_line_ is None or t_line_ == ''):
                break
            t_tokens_ = t_line_.split()
            if (t_current_phase_ == 0): #Init
                t_dep_shortcode_ = t_tokens_[2]
                t_dep_base_pricetype_ = t_tokens_[3]
                t_current_phase_ = 1
                 
            elif (t_current_phase_ == 1): #PreModel
                if (t_tokens_[1] == 'LINEAR'):
                    t_model_math_ = LinearModelAggregator(_watch_, _model_filename_)
                t_current_phase_ = 2
                
            elif (t_current_phase_ == 2): #PostModel
                t_current_phase_ = 3
                
            elif (t_current_phase_ == 3): #IndicatorStarted
                print(t_tokens_)
                if (t_tokens_[0] == 'INDICATOR'):
                    t_weight_ = float(t_tokens_[1])
                    t_indicator_ = ModelCreator.GetIndicatorFromTokens(_watch_, t_tokens_, t_dep_base_pricetype_)
                    if (t_indicator_ is not None):
                        t_readiness_required_ = t_indicator_.GetReadinessRequired(t_dep_shortcode_, t_tokens_)
                        t_model_math_.AddIndicator(t_indicator_, t_weight_, t_readiness_required_)
                    else:
                        print 'Error in Indicator Creation'
                        exit()
                else:
                    t_model_math_.SetBasePrice()
                    t_model_math_.FinishCreation()
                    t_current_phase_ = 4
            
            elif (t_current_phase_ == 4): #IndicatorEnded
                break
        print('-------------------------------')
        return t_model_math_