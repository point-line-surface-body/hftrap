import sys
import signal
from os.path import expanduser
from CDef.defines import BASESYSINFODIR

SECONDS_TO_PREP = 1800

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
    
    

    
    return

if __name__ == "__main__":
    __main__()