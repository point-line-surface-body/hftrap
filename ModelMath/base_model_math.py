from Indicators.indicator_listener import IndicatorListener
from MarketAdapter.security_market_view_on_ready_listener import SecurityMarketViewOnReadyListener

class BaseModelMath(IndicatorListener, SecurityMarketViewOnReadyListener):

	def __init__(self, _watch_, _model_filename_):
		self.watch = _watch_
		self.model_filename = _model_filename_
		self.is_ready_vec = []
		self.readiness_required_vec = []
		self.is_ready = False
		self.last_is_ready = False
		self.model_stdev = 1.00 # Check whether it is needed
		self.model_math_listener_vec = [] # What is this
		self.indicator_vec = []

	def GetModelFileName(self):
		return self.model_filename;
	
	def AddIndicator(self, _indicator_, _weight_, _readiness_required_):
		_indicator_.AddIndicatorListener(len(self.indicator_vec), self, _weight_) # Why?
		self.indicator_vec.append(_indicator_)
		if (_indicator_.isIndicatorReady()):
			self.is_ready_vec.append(True)
			self.readiness_required_vec.append(False)
		else:
			self.is_ready_vec.append(False)
			self.readiness_required_vec.append(_readiness_required_)
			self.is_ready = False

	def AddListener(self, _model_math_listener_):
		self.model_math_listener_vec.append(_model_math_listener_)
		
	def PropagateNewTargetPrice(self, _new_target_, _new_sum_vars_):
		for i in range(0, len(self.model_math_listener_vec)):
			self.model_math_listener_vec[i].UpdateTarget(_new_target_, _new_sum_vars_)