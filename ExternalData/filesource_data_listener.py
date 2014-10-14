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
        
        return
    
    def ProcessThisEvent(self):
        return

    def SetNextTimeStamp(self):
        '''@Ashwin Can it be less than zero?'''
        if (self.events_left <= 0):
            self.events_left = 0
            '''Why Non Intermediate?'''
            found_non_intermediate_event = False
            while (not found_non_intermediate_event):
                if (self.file.read(self.next_event, )):
                    self.next_event_timestamp = 0
                    return False
                if (self.next_event.time != 0):
                    next_non_intermediate_time = self.next_event.time
                    found_non_intermediate_event = True
            self.event_queue.append(self.next_event)
            self.events_left += 1
        if (self.events_left > 0):
            self.next_event = self.event_queue_[0]
            self.next_event_timestamp = next_non_intermediate_time
            self.events_left -= 1;
            self.event_queue.pop()
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