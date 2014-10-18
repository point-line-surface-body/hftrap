import sys
sys.path.append('/Users/ashwink/Documents/workspace/hftrap')
from DebugUtils.print_vector import print_vector
from CommonTradeUtils.watch import Watch
from ModelMath.model_creator import ModelCreator
from InitCommon.strategy_desc import StrategyDesc
from ExternalData.historical_dispatcher import HistoricalDispatcher
from MarketAdapter.security_market_view import SecurityMarketView
from CommonTradeUtils.market_update_manager import MarketUpdateManager
from ExternalData.filesource import FileSource
from ExecLogic.directional_aggressive_trading import DirectionalAggressiveTrading
from OrderManager.base_trader import BaseTrader
from OrderManager.base_order_manager import BaseOrderManager
from MarketAdapter.shortcode_security_market_view_map import ShortcodeSecurityMarketViewMap
from OrderManager.base_sim_market_maker import BaseSimMarketMaker

def __main__():
     
    if (len(sys.argv) < 3):
        print 'USAGE: EXEC STRATEGY_FILE_NAME TRADING_DATE'
        exit(0)

    strategy_desc_filename_ = sys.argv[1] # decide the no. of arguments and order of arguments
    tradingdate_ = sys.argv[2]

    watch_ = Watch(tradingdate_)
    ShortcodeSecurityMarketViewMap.watch_ = watch_

    strategy_desc_ = StrategyDesc(strategy_desc_filename_, tradingdate_)
    strategy_desc_.Dump()
    dependant_shortcode_ = strategy_desc_.strategy_vec_[0].dep_shortcode_
    print(dependant_shortcode_)

    source_shortcode_vec_ = [] # vector of all sources which we need data for or are trading
    shortcode_to_sid_map_ = {}
    smv_vec_ = []

    source_shortcode_vec_.append(dependant_shortcode_)
    model_filename_ = strategy_desc_.strategy_vec_[0].model_filename_

    print_vector(source_shortcode_vec_)
    ModelCreator.CollectShortCodes(model_filename_, source_shortcode_vec_)

    for i_ in range(0, len(source_shortcode_vec_)):
        shortcode_to_sid_map_[source_shortcode_vec_[i_]] = i_
        #smv_ = SecurityMarketView(watch_, source_shortcode_vec_[i_], i_)
        smv_vec_.append(ShortcodeSecurityMarketViewMap.StaticGetSecurityMarketView(source_shortcode_vec_[i_]))
    base_model_math_ = ModelCreator.CreateModelMathComponent(watch_, model_filename_) # need to update smv_vec in this function itself

    sim_market_maker_ = BaseSimMarketMaker(watch_, smv_vec_[0])
    base_trader_ = BaseTrader(sim_market_maker_)
    strategy_desc_.strategy_vec_[0].dep_market_view_ = smv_vec_[0]
    strategy_desc_.strategy_vec_[0].p_base_trader_ = sim_market_maker_
    
    order_manager_ = BaseOrderManager(watch_, base_trader_, smv_vec_[0], strategy_desc_.strategy_vec_[0].runtime_id_)
        
    if (strategy_desc_.strategy_vec_[0].strategy_name_ == 'DirectionalAggressiveTrading'):
        strategy_desc_.strategy_vec_[0].exec_ = DirectionalAggressiveTrading(watch_, smv_vec_[0], order_manager_, 
                                                                             strategy_desc_.strategy_vec_[0].param_filename_, 
                                                                             strategy_desc_.strategy_vec_[0].trading_start_time_mfm_, 
                                                                             strategy_desc_.strategy_vec_[0].trading_end_time_mfm_,
                                                                             strategy_desc_.strategy_vec_[0].runtime_id_, 
                                                                             source_shortcode_vec_) 

    historical_dispatcher_ = HistoricalDispatcher()

    for shortcode_ in source_shortcode_vec_:
        file_source_ = FileSource(watch_, shortcode_, smv_vec_[shortcode_to_sid_map_[shortcode_]], tradingdate_)
        historical_dispatcher_.AddExternalDataListener(file_source_)

# 
#     base_pnl = BasePnl(watch_, order_manager_, sid_to_shortcode_ptr_map_[0])
# 
#     
# 
    base_model_math_.AddListener(strategy_desc_.strategy_vec_[0].exec_)
    strategy_desc_.strategy_vec_[0].exec_.SetModelMathComponent(base_model_math_)
    for smv_ in smv_vec_:
        smv_.SubscribeOnReady(base_model_math_)
    
    market_update_manager_ = MarketUpdateManager.GetUniqueInstance(watch_, smv_vec_,tradingdate_ )
    market_update_manager_.start()

    '''Run Historical Dispatcher'''
    data_seek_time_ = strategy_desc_.GetMinStartTime() # subtract some preparation time
    historical_dispatcher_.SeekHistFileSourcesTo(data_seek_time_)
    historical_dispatcher_end_time_ = strategy_desc_.GetMaxEndTime() # add 1 hour
    historical_dispatcher_.RunHist(historical_dispatcher_end_time_)

    '''Print Results'''
    #strategy_desc_.strategy_vec_[0].exec_.ReportResults(trades_writer_)
    
if __name__ == "__main__":
    __main__()