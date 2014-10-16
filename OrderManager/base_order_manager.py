from OrderManager.base_order import BaseOrder

class BaseOrderManager:
    
    watch_
    dep_shortcode_
    base_trader_
    bid_int_price_adjustment_
    ask_int_price_adjustment_
    
    bid_order_vec_
    order_vec_top_bid_index_
    order_vec_bottom_bid_index_
    
    sum_bid_confirmed_
    confirmed_top_bid_index_
    confirmed_bottom_bid_index_
    
    sum_bid_confirmed_
    unconfirmed_top_bid_index_
    uncomfirmed_bottom_bid_index_
    
    def __init__(self, _watch_, _base_trader_, _dep_shortcode_, _min_price_increment_):
        self.watch_ = _watch_
        self.base_trader_ = _base_trader_
        self.dep_shortcode_ = _dep_shortcode_
        
        self.initial_adjustment_set_ = False
        self.bid_int_price_adjustment_ = 0
        self.ask_int_price_adjustment_ =  0
        self.order_vec_top_bid_index_  = -1
        self.order_vec_bottom_bid_index_ = -1
        self.confirmed_top_bid_index_ = -1
        self.confirmed_bottom_bid_index_ = -1
        self.unconfirmed_top_bid_index_ = -1
        self.unconfirmed_bottom_bid_index_ = -1
        self.order_vec_top_ask_index_ = -1
        self.order_vec_bottom_ask_index_ = -1
        self.confirmed_top_ask_index_ = -1
        self.confirmed_bottom_ask_index_ = -1
        self.unconfirmed_top_ask_index_ = -1
        self.unconfirmed_bottom_ask_index_ = -1
        self.unsequenced_bids_ = []
        self.unsequenced_asks_ = []
        self.external_cancel_all_outstanding_orders_ = False
        self.num_unconfirmed_orders_ = 0
        self.s_p_position_change_listener_ = []
        self.position_change_listener_vec_ = []
        self.s_p_execution_listener_ = []
        self.execution_listener_vec_ = []
        self.s_p_order_change_listener_ = []
        self.order_change_listener_vec_ = []
        self.s_p_cxl_reject_listener_ = []
        self.cxl_reject_listener_vec_ = []
        self.s_p_reject_funds_listener_ = []
        self.reject_due_to_funds_listener_vec_ = []
        self.client_position_ = 0
        self.global_position_ = 0
        self.map_clean_counter_ = 0
        self.sum_bid_sizes_ = 0
        self.sum_ask_sizes_ = 0
        self.num_self_trades_ = 0
        self.trade_volume_ = 0
        self.last_maps_cleaned_msecs_ = 0
        self.last_top_replay_msecs_ = 0
        self.queue_sizes_needed_ = False
        self.best_bid_int_price_ = 0
        self.best_ask_int_price_ = 0
        self.supporting_order_filled_= 0
        self.best_level_order_filled_ = 0
        self.aggressive_order_filled_ = 0
        self.improve_order_filled_ = 0
        self.total_size_placed_ = 0
        self.send_order_count_ = 0
        self.cxl_order_count_ = 0
        self.security_id_to_last_position_( sec_name_indexer_.NumSecurityId ( ) , kInvalidPosition ) , security_position_ ( 0 ) ,// To maintain positions for all contracts of this security.
        self.p_ticks_to_keep_bid_int_price_ = None
        self.p_ticks_to_keep_ask_int_price_ = None
        self.throttle_manager_ = None
        
        bid_order_vec_.resize ( ORDER_MANAGER_INT_PRICE_RANGE, std::vector < BaseOrder * > ( ) );
        sum_bid_confirmed_.resize ( ORDER_MANAGER_INT_PRICE_RANGE, 0 );
        sum_bid_unconfirmed_.resize ( ORDER_MANAGER_INT_PRICE_RANGE, 0 );


        ask_order_vec_.resize ( ORDER_MANAGER_INT_PRICE_RANGE, std::vector < BaseOrder * > ( ) );
        sum_ask_confirmed_.resize ( ORDER_MANAGER_INT_PRICE_RANGE, 0 );
        sum_ask_unconfirmed_.resize ( ORDER_MANAGER_INT_PRICE_RANGE, 0 );
        return
    
    def GetBidIndex(self, _int_price_):
        return _int_price_ - self.bid_int_price_adjustment_
    
    def GetAskIndex(self, _int_price_):
        return _int_price_ - self.ask_int_price_adjustment_
    
    def GetBidIndexAndAdjustIntPrice(self, _int_price_):
        t_bid_index_ = self.GetBidIndex(_int_price_)
        # Do some adjustment
        return t_bid_index_
    
    def GetAskIndexAndAdjustIntPrice(self, _int_price_):
        t_ask_index_ = self.GetAskIndex(_int_price_)
        # Do some adjustment
        return t_ask_index_
    
    def SendTrade(self, _price_, _int_price_, _size_requested_, _buysell_):
        if (_size_requested_ <= 0):
            print 'SendTrade: _size_requested_ <= 0'
            return
        order = BaseOrder()
        order.security_name = self.shortcode_
        order.buy_sell = _buysell_
        order.price = _price_
        order.int_price = _int_price_
        order.size_requested = _size_requested_
        order.size_remaining = 0
        order.order_status = None
        
        if (_buysell_ == 0): # Buy
            t_bid_index_ = self.GetBidIndexAndAdjustIntPrice(_int_price_)
            self.sum_bid_unconfirmed_[t_bid_index_] += _size_requested_
            self.AdjustTopBottomUnconfirmedBidIndexes(t_bid_index_)
            self.unsequenced_bids_.append(order)
            self.num_unconfirmed_orders_ += 1
            self.sum_bid_sizes_ += _size_requested_
        else:
            t_ask_index_ = self.GetAskIndexAndAdjustIntPrice(_int_price_)
            self.sum_ask_unconfirmed_[t_ask_index_] += _size_requested_
            self.AdjustTopBottomUnconfirmedAskIndexes(t_ask_index_)
            self.unsequenced_bids_.append(order)
            self.num_unconfirmed_orders_ += 1
            self.sum_ask_sizes_ += _size_requested_
            
        self.base_trader_.SendTrade(order)
        
        self.total_size_placed_ += _size_requested_
        self.send_order_count += 1    
        