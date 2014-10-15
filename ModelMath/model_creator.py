
class ModelCreator():
    
    def __init__(self):
        return
    
    @staticmethod
    def CollectShortCodes(_model_filename_, _source_shortcodes_vec_) :
        t_dep_shortcode_ = 'NONAME'
        t_indicator_map_ = {}
        t_model_file_ = open(_model_filename_, 'r')
        t_current_phase_ = 0
        while (1):
            t_line_ = t_model_file_.readline()
            t_tokens_ = t_line_.split()
            if (t_current_phase_ == 0):
                if ((t_tokens_[0] == 'MODELINIT') == 0):
                    
        return
    
    def CreateModelMathComponent(self, watch_, _model_filename_):
        return