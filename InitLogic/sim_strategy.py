import sys
from CommonTradeUtils.watch import Watch
from ModelMath.model_creator import ModelCreator
#from ExecLogic.base_trading import BaseTrading
from InitCommon.strategy_desc import StrategyDesc
from ExternalData.filesource import FileSource
from ExternalData.historical_dispatcher import HistoricalDispatcher
from MarketAdapter.security_market_view import SecurityMarketView
import OrderManager
from CommonTradeUtils.market_update_manager import MarketUpdateManager
from SimMarketMaker.price_level_sim_market_maker import PriceLevelSimMarketMaker
from ExternalData.filesource_data_listener import FileSource


SECONDS_TO_PREP = 1800
MIN_YYYYMMDD = 20090920
MAX_YYYYMMDD = 20141225

def __main__():
     
    if (len(sys.argv) < 3):
        print 'USAGE: EXEC STRATEGY_FILE_NAME TRADING_DATE'
        exit(0)

    strategy_desc_filename_ = sys.argv[1] # decide the no. of arguments and order of arguments
    tradingdate_ = sys.argv[2]

    strategy_desc_ = StrategyDesc(strategy_desc_filename_, tradingdate_)
    watch_ = Watch(tradingdate_)
    dependant_shortcode_ = strategy_desc_.strategy_vec_[0].dep_shortcode_

    source_shortcode_vec_ = [] # vector of all sources which we need data for or are trading
    shortcode_to_sid_map_ = {}
    smv_vec_ = []

    source_shortcode_vec_.append(dependant_shortcode_)
    model_filename_ = strategy_desc_.strategy_vec_[0].model_filename_

    ModelCreator.CollectShortCodes(model_filename_, source_shortcode_vec_)
    
    for i_ in range(0, len(source_shortcode_vec_)):
        shortcode_to_sid_map_[source_shortcode_vec_[i_]] = i_
        smv_ = SecurityMarketView(watch_, source_shortcode_vec_[i_], i_)
        smv_vec_.append(smv_)

    historical_dispatcher_ = HistoricalDispatcher()

    for shortcode_ in source_shortcode_vec_:
        file_source_ = FileSource(watch_, shortcode_, smv_vec_[shortcode_to_sid_map_[shortcode_]], tradingdate_)
        historical_dispatcher_.AddExternalDataListener(file_source_)

#     sim_market_maker_ = PriceLevelSimMarketMaker(watch_, sid_to_smv_ptr_map_[0])
#     base_trader = SimTrader(sim_market_maker)
#     strategy_desc_.strategy_vec_[0].dep_market_view_ = sid_to_smv_ptr_map_[0]
#     strategy_desc_.strategy_vec_[0].p_base_trader_ = sim_market_maker_
# 
#     order_manager_ = OrderManager(watch_, sid_to_shortcode_ptr_map_[0], strategy_desc_.strategy_vec_[0].p_base_trader_)
#     base_pnl = BasePnl(watch_, order_manager_, sid_to_shortcode_ptr_map_[0])
# 
#     base_model_math_ = ModelCreator.CreateModelMathComponent(watch_, model_filename_)
# 
#     base_model_math_.AddListener(strategy_desc_.strategy_vec_[0].exec_)
#     strategy_desc_.strategy_vec_[0].exec_.SetModelMathComponent(base_model_math_)
    
    market_update_manager_ = MarketUpdateManager() # initialise with proper arguments
    market_update_manager_.start();

    '''Run Historical Dispatcher'''
    data_seek_time_ = strategy_desc_.GetMinStartTime() # subtract some preparation time
    historical_dispatcher_.SeekHistFileSourcesTo(data_seek_time_)
    historical_dispatcher_end_time_ = strategy_desc_.GetMaxEndTime() # add 1 hour
    historical_dispatcher_.RunHist(historical_dispatcher_end_time_)
