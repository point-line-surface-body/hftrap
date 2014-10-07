from abc import ABCMeta
from abc import abstractmethod

# Anyone who wishes to listen to ModelMath must extend this class
class ModelMathListener():
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def UpdateTarget(self, _new_target_, _new_sum_vars_):
        return
    
    @abstractmethod
    def TargetNotReady(self):
        return