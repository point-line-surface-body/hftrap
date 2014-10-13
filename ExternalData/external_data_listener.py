class ExternalDataListener():

    def __init__(self):
        self.next_event_timestamp = 0
        return
    
    def __del__(self):
        return
    
    def __lt__(self, other):
        return self.NextEventTimestamp() < other.NextEventTimestamp()
    
    def socket_file_descriptor(self):
        return
    
    def SeekToFirstEventAfter(self, time, has_events):
        return
    
    def ComputeEarliestDataTimestamp(self, has_events):
        return
    
    def ProcessAllEvents(self):
        return
    
    def ProcessEventsTill(self, _end_time_):
        return
        
    def NextEventTimestamp(self):
        return self.next_event_timestamp