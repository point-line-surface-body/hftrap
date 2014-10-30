from InitLogic.paramset import ParamSet
from ExecLogic.trade_vars import TradeVars
from ModelMath.base_model_math import ModelMathListener
from MarketAdapter.security_market_view import SecurityMarketViewChangeListener

class BaseTrading(ModelMathListener, SecurityMarketViewChangeListener): #extends many classes.. add here

	def __init__(self, _watch_, _dep_market_view_, _order_manager_, _paramfilename_, _trading_start_time_, 
                 _trading_end_time_, _runtime_id_, _model_source_shortcode_vec_):
		self.watch_ = _watch_
		self.dep_market_view_ = _dep_market_view_
		self.param_set_ = ParamSet(_paramfilename_)
		self.current_tradevarset_ = TradeVars()
		self.InitializeTradeVarSet()
		self.order_manager_ = _order_manager_
		self.trading_start_time_ = _trading_start_time_
		self.trading_end_time_ = _trading_end_time_
		self.runtime_id_ = _runtime_id_
		self.my_position_ = 0
		self.is_ready_ = False
		self.should_be_getting_flat_ = False
		self.get_flat_due_to_close_ = False
		self.get_flat_due_to_max_position_ = False
		self.get_flat_due_to_max_loss_ = False
		self.get_flat_due_to_max_opentrade_loss_ = False
		self.get_flat_due_to_max_pnl_ = False
		
		self.best_nonself_bid_price_ = 0
		self.best_nonself_bid_int_price_ = 0
		self.best_nonself_bid_size_ = 0
		self.best_nonself_ask_price_ = 0
		self.best_nonself_ask_int_price_ = 0
		self.best_nonself_ask_size_ = 0
		
		self.target_price_ = 0
		self.targetbias_numbers_ = 0
		self.model_stdevs_ = 0
		
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
		
		self.last_buy_msecs_ = 0
		self.last_buy_int_price_ = 0
		self.last_sell_msecs_ = 0
		self.last_sell_int_price_ = 0
		self.last_agg_buy_msecs_ = 0
		self.last_agg_sell_msecs_ = 0
		
		self.dep_market_view_.SubscribeL1Only(self)
		self.count_ = 0
		return
	
	def OnPositionUpdate(self, _new_position_):
		self.my_position_ = _new_position_
		self.current_tradevarset_.l1bid_trade_size_ = self.param_set_.unit_trade_size_
		self.current_tradevarset_.l1ask_trade_size_ = self.param_set_.unit_trade_size_
		if (self.my_position_ + self.current_tradevarset_.l1bid_trade_size_ > self.param_set_.max_position_):
			self.current_tradevarset_.l1bid_trade_size_ = 0
		if (self.my_position_ - self.current_tradevarset_.l1ask_trade_size_ < - self.param_set_.max_position_):
			self.current_tradevarset_.l1ask_trade_size_ = 0
	
	def TradingLogic(self):
		return
	
	def SetModelMathComponent(self, _base_model_math_):
		self.base_model_math_ = _base_model_math_
	
	def ReportResults(self):
		return
	
	def GetPosition(self):
		return self.my_position_
	
	def NonSelfMarketUpdate(self):
		self.best_nonself_bid_price_ = self.dep_market_view_.bestbid_price()
		self.best_nonself_bid_int_price_ = self.dep_market_view_.bestbid_int_price()
		self.best_nonself_bid_size_ = self.dep_market_view_.bestbid_size()
		self.best_nonself_ask_price_ = self.dep_market_view_.bestask_price()
		self.best_nonself_ask_int_price_ = self.dep_market_view_.bestask_int_price()
		self.best_nonself_ask_size_ = self.dep_market_view_.bestask_size()
		
	def OnMarketUpdate(self, _market_update_info_):
		self.count_ += 1
		#print 'BT.OnMarketUpdate: '+str(self.count_)
		self.NonSelfMarketUpdate()
		
	def OnTradePrint(self, _trade_print_info_, _market_update_info_):
		self.NonSelfMarketUpdate()
	
	def UpdateTarget(self, _new_target_, _new_sum_vars_):
		#print('BT.UpdateTarget'),
		if (not self.is_ready_):
			print('BT is not ready for the first time')
			print(str(self.watch_.GetMsecsFromMidnight())+' '+str(self.trading_start_time_))
			print(str(_new_target_))
			#print(self.dep_market_view_)
			print(self.dep_market_view_.bestbid_price())
			print(self.dep_market_view_.bestask_price())
			if ((self.watch_.GetMsecsFromMidnight() > self.trading_start_time_) and
				(self.dep_market_view_.is_ready_) and
				(_new_target_ >= self.dep_market_view_.bestbid_price()) and
				(_new_target_ <= self.dep_market_view_.bestask_price())):
				self.is_ready_ = True
				#print('BT is now ready')
		else:
			#print('BT is ready')
			self.target_price_ = _new_target_
			self.targetbias_numbers_ = _new_sum_vars_
			self.ShouldBeGettingFlat()
			if (not self.should_be_getting_flat_):
				self.TradingLogic()
				'''Why?'''
				#self.CallPlaceCancelNonBestLevels()
			else:
				self.GetFlatTradingLogic()
		return
	
	def ShouldBeGettingFlat(self):
		#print self.watch_.GetMsecsFromMidnight(), self.trading_end_time_
		if (self.watch_.GetMsecsFromMidnight() > self.trading_end_time_):
			self.get_flat_due_to_close_ = True
		self.should_be_getting_flat_ = self.get_flat_due_to_close_ or self.get_flat_due_to_max_loss_ or self.get_flat_due_to_max_opentrade_loss_ or self.get_flat_due_to_max_pnl_ or self.get_flat_due_to_max_position_
	
	def GetFlatTradingLogic(self):
		print'GetFlat'
		t_position_ = self.my_position_
		if (t_position_ == 0):
			self.order_manager_.CancelAllOrders()
		elif (t_position_ > 0):
			#self.order_manager_.CancelAllBidOrders()
			self.order_manager_.CancelAllOrders()
			#self.order_manager_.CancelAsksBelowIntPrice(self.best_nonself_ask_int_price_)
			self.order_manager_.SendTrade(self.best_nonself_bid_price_, self.best_nonself_bid_int_price_, t_position_, 'S')
		else:
			#self.order_manager_.CancelAllAskOrders()
			#self.order_manager_.CancelBidsBelowIntPrice(self.best_nonself_bid_int_price_)
			self.order_manager_.CancelAllOrders()
			self.order_manager_.SendTrade(self.best_nonself_ask_price_, self.best_nonself_ask_int_price_, - t_position_, 'B')
			
	def UpdatePosition(self):
		self.my_position_ += self.position_offset_
			
	def InitializeTradeVarSet(self):
		self.current_tradevarset_.l1bid_aggressive = self.param_set_.bid_aggress_threshold_ * self.dep_market_view_.MinPriceIncrement()
		self.current_tradevarset_.l1bid_improve_ = self.param_set_.bid_improve_threshold_ * self.dep_market_view_.MinPriceIncrement()
		self.current_tradevarset_.l1bid_improve_keep_ = self.param_set_.bid_improve_keep_threshold_ * self.dep_market_view_.MinPriceIncrement()
		self.current_tradevarset_.l1bid_keep_ = self.param_set_.bid_keep_threshold_ * self.dep_market_view_.MinPriceIncrement()
		self.current_tradevarset_.l1bid_place_ = self.param_set_.bid_place_threshold_ * self.dep_market_view_.MinPriceIncrement()
		self.current_tradevarset_.l1bid_trade_size_ = self.param_set_.unit_trade_size_
		
		self.current_tradevarset_.l1ask_aggressive = self.param_set_.ask_aggress_threshold_ * self.dep_market_view_.MinPriceIncrement()
		self.current_tradevarset_.l1ask_improve_ = self.param_set_.ask_improve_threshold_ * self.dep_market_view_.MinPriceIncrement()
		self.current_tradevarset_.l1ask_improve_keep_ = self.param_set_.ask_improve_keep_threshold_ * self.dep_market_view_.MinPriceIncrement()
		self.current_tradevarset_.l1ask_keep_ = self.param_set_.ask_keep_threshold_ * self.dep_market_view_.MinPriceIncrement()
		self.current_tradevarset_.l1ask_place_ = self.param_set_.ask_place_threshold_ * self.dep_market_view_.MinPriceIncrement()
		self.current_tradevarset_.l1ask_trade_size_ = self.param_set_.unit_trade_size_
