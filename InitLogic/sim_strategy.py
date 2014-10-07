import sys
import signal
from os.path import expanduser
from CDef.defines import BASESYSINFODIR
from InitCommon.strategy_desc import *
from CommonTradeUtils.watch import Watch
from ModelMath.model_creator import ModelCreator
from ExecLogic.base_trading import BaseTrading

SECONDS_TO_PREP = 1800
MIN_YYYYMMDD = 20090920
MAX_YYYYMMDD = 20141225

def termination_handler(signum):
    exit()

def ParseCommandLineParams(*argv):
    return

def __main__():
    signal.signal(signal.SIGINT, termination_handler)
    signal.signal(signal.SIGSEGV, termination_handler)
    signal.signal(signal.SIGILL, termination_handler)
    signal.signal(signal.SIGFPE, termination_handler)
    livetrading_ = False
    tradingdate_ = 0
    progid_ = 0
    strategy_desc_filename_ = ""
    tradesfilename_ = ""
    home = expanduser("~")
    network_account_info_filename_ = home +  BASESYSINFODIR + "TradingInfo/NetworkInfo/network_account_info_filename.txt"
    market_model_index_ = 0
    secs_to_prep_ = SECONDS_TO_PREP
    strat_start_time_ =0
    #HFSAT::SecurityNameIndexer & sec_name_indexer_ = HFSAT::SecurityNameIndexer::GetUniqueInstance ( ) ;
    source_shortcode_vec_ = []
    ors_needed_by_indicators_vec_ = []
    dependant_shortcode_vec_ = []
    sid_to_marketdata_needed_map_ = []
    #ParseCommandLineParams ( livetrading_, tradingdate_, strategy_desc_filename_, progid_,network_account_info_filename_, market_model_index_, secs_to_prep_, strat_start_time_ )
    strategy_desc_ = StrategyDesc(strategy_desc_filename_,tradingdate_)
    watch_ = Watch(tradingdate_)
    modelfilename_source_shortcode_vec_map_ = [] #map from modelfilename_ to source_shortcode_vec_ to pass to setup ModelMath as listener to market_data events
    modelfilename_ors_needed_by_indicators_vec_map_ = [] #map from modelfilename_ to source_shortcode_vec_ to pass to setup ModelMath as listener to OrderRouting message events
    for i in range(len(strategy_desc_.strategy_vec_)) :
        if strategy_desc_.strategy_vec_[i].modelfilename_ not in modelfilename_source_shortcode_vec_map_:
            if strategy_desc_.strategy_vec_[i].dep_shortcode_ not in dependant_shortcode_vec_:
                dependant_shortcode_vec_.append(strategy_desc_.strategy_vec_[i].dep_shortcode_)
            if strategy_desc_.strategy_vec_[i].dep_shortcode_ not in source_shortcode_vec_:
                source_shortcode_vec_.append(strategy_desc_.strategy_vec_[i].dep_shortcode_)
            ModelCreator.CollectShortCodes(watch_,strategy_desc_.strategy_vec_[i].modelfilename_,modelfilename_source_shortcode_vec_map_ [ strategy_desc_.strategy_vec_[i].modelfilename_ ],modelfilename_ors_needed_by_indicators_vec_map_ [ strategy_desc_.strategy_vec_[i].modelfilename_ ],False)
            if modelfilename_source_shortcode_vec_map_ [ strategy_desc_.strategy_vec_[i].modelfilename_ ] not in source_shortcode_vec_:
                source_shortcode_vec_.append(modelfilename_source_shortcode_vec_map_ [ strategy_desc_.strategy_vec_[i].modelfilename_ ])
            if modelfilename_ors_needed_by_indicators_vec_map_ [ strategy_desc_.strategy_vec_[i].modelfilename_ ] not in ors_needed_by_indicators_vec_:
                ors_needed_by_indicators_vec_.append(modelfilename_ors_needed_by_indicators_vec_map_ [ strategy_desc_.strategy_vec_[i].modelfilename_ ])
            BaseTrading.CollectORSShortCodes(strategy_desc_.strategy_vec_[i].strategy_name_,strategy_desc_.strategy_vec_[i].dep_shortcode_, source_shortcode_vec_, ors_needed_by_indicators_vec_)
            if strategy_desc_.strategy_vec_[i].dep_shortcode_ not in ors_needed_by_indicators_vec_ :
                ors_needed_by_indicators_vec_.append(strategy_desc_.strategy_vec_[i].dep_shortcode_)




    return

if __name__ == "__main__":
    __main__()