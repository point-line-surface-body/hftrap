from InitCommon.paramset import ParamSet
from ExecLogic.trade_vars import TradeVars
from __builtin__ import None

class BaseTrading(): #extends many classes.. add here

	def __init__(self, _watch_, _dep_market_view_, _order_manager_, _paramfilename_, _trading_start_time_, 
                 _trading_end_time_, _runtime_id_, _model_source_shortcode_vec_):
		self.param_set_ = ParamSet(_paramfilename_)
		self.current_tradevarset_ = TradeVars()
		self.InitializeTradeVarSet()
		self.dep_market_view_ = _dep_market_view_
		self.order_manager_ = _order_manager_
		self.trading_start_time_ = _trading_start_time_
		self.trading_end_time_ = _trading_end_time_
		self.runtime_id_ = _runtime_id_
		self.myposition_ = 0
		self.should_be_getting_flat_ = False
		self.get_flat_due_to_close_ = False
		self.get_flat_due_to_max_position_ = False
		self.get_flat_due_to_max_loss_ = False
		self.get_flat_due_to_max_opentrade_loss_ = False
		self.get_flat_due_to_max_pnl_ = False
		
		self.best_non_self_bid_price_ = None
		self.best_non_self_bid_int_price_ = None
		self.best_non_self_bid_size_ = None
		self.best_non_self_ask_price_ = None
		self.best_non_self_ask_int_price_ = None
		self.best_non_self_ask_size_ = None
		
		self.target_price_ = None
		self.target_bias_numbers_ = None
		self.model_stdevs_ = None
		
		self.top_bid_place_ = False
		self.top_bid_keep_ = False
		self.top_ask_place_ = False
		self.top_ask_keep_ = False

		self.top_bid_improve_ = False
		self.top_ask_lift_ = False
		self.top_ask_improve_ = False
		self.top_bid_hit_ = False

		self.bid_improve_keep_ = False
		self.ask_improve_keep_ = False
		
		self.last_buy_msecs_
		self.last_buy_int_price_;
		self.last_sell_msecs_;
		self.last_sell_int_price_;
		self.last_agg_buy_msecs_ ;
		self.last_agg_sell_msecs_ ;
		return
	
	def TradingLogic(self):
		return
	
	def OnMarketUpdate(self):
		return
	
	def OnTradePrint(self):
		return		
	
	def SetModelMathComponent(self, _base_model_math_):
		self.base_model_math_ = _base_model_math_
	
	def ReportResults(self):
		return
	
	def InitializeTradeVarSet(self):
		self.current_tradevarset_.l1bid_aggressive = self.param_set_.bid_aggress_threshold_
		self.current_tradevarset_.l1bid_improve_ = self.param_set_.bid_improve_threshold_
		self.current_tradevarset_.l1bid_improve_keep_ = self.param_set_.bid_improve_keep_threshold_
		self.current_tradevarset_.l1bid_keep_ = self.param_set_.bid_keep_threshold_
		self.current_tradevarset_.l1bid_place_ = self.param_set_.bid_place_threshold_
		self.current_tradevarset_.l1bid_trade_size_ = self.param_set_.unit_trade_size_
		
		self.current_tradevarset_.l1ask_aggressive = self.param_set_.ask_aggress_threshold_
		self.current_tradevarset_.l1ask_improve_ = self.param_set_.ask_improve_threshold_
		self.current_tradevarset_.l1ask_improve_keep_ = self.param_set_.ask_improve_keep_threshold_
		self.current_tradevarset_.l1ask_keep_ = self.param_set_.ask_keep_threshold_
		self.current_tradevarset_.l1ask_place_ = self.param_set_.ask_place_threshold_
		self.current_tradevarset_.l1ask_trade_size_ = self.param_set_.unit_trade_size_
		
	@staticmethod
	def CollectORSShortCodes(*args): # how many arguments to keep
		return