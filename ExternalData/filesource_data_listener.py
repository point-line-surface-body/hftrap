from ExternalData.external_data_listener import ExternalDataListener
from TradingPlatform.get_data_file_name import GetFileSourceName

class FileSource(ExternalDataListener):
    
    def __init__(self, _shortcode_):
        self.shortcode = _shortcode_
        self.file_name = GetFileSourceName(_shortcode_)
        
        