from ExternalData.external_data_listener import ExternalDataListener
from TradingPlatform.get_data_file_name import GetFileSourceName

class FileSource(ExternalDataListener):
    
    def __init__(self, _shortcode_):
        self.shortcode = _shortcode_
        self.file_name = GetFileSourceName(_shortcode_)
        self.file = open(self.file_name)
        
    def __del__(self):
        return
    
    def SeekToFirstEventAfter(self, time, has_events):
        return ExternalDataListener.SeekToFirstEventAfter(self, time, has_events)
    
    def ProcessThisEvent(self):
        return
    
    def SetNextTimeStamp(self):
        if (self.events_left <= 0):
            events_left = 0
        found_non_intermediate_event = False
        while (not found_non_intermediate_event):
            if (self.file.read(&next_event, )):
                next_event_timestamp_ = 0
                return False
            if (next_event_.time != 0):
                next_non_intermediate_time = next_event.time
                found_non_intermediate_event = True
            self.event_queue.push_back(next_event)
            events_left += 1

          if (self.events_left > 0):
              next_event = event_queue_[0]
              next_event_timestamp = next_non_intermediate_time
              events_left -= 1;
              event_queue.erase(event_queue.begin())
              return True
          
        return True
    
    def ProcessAllEvents(self):
        while (1):
            self.ProcessThisEvent()
            if (not self.SetNextTimeStamp()):
                return
    
    def ProcessEventsTill(self, _end_time_):
        while (self.next_event_timestamp <= _end_time_):
            self.ProcessThisEvent()
            if (not self.SetNextTimeStamp()):
                return