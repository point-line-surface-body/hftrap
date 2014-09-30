import heapq

class HistoricalDispatcher() :

	first_event_enqueued = False
	external_data_listener_vec = []
	prev_external_data_listerner_vec = []    
	
	def __init__(self):
		return

	def __del__(self):
		self.DeleteSource()
		
	def AddExternalDataListener(self, new_listener):
		self.external_data_listener_vec.append(new_listener)

	def RunHist(self, endtime): # endtime = something by default
		if ( not self.first_event_enqueued):
			for it in range(0, len(self.external_data_listener_vec)):
				hasevents = self.external_data_listener_vec[it].ComputeEarliestDataTimestamp()
				if ( not hasevents):
					self.prev_external_data_listerner_vec.append(self.external_data_listener_vec[it])
					self.external_data_listener_vec.remove(it) # correct this
			self.first_event_enqueued = True

		if (len(self.external_data_listener_vec) == 1):
			# No need to make heap
			self.external_data_listener_vec[0].ProcessEventsTill(endtime)
			self.prev_external_data_listerner_vec.append(self.external_data_listener_vec[0])
			self.external_data_listener_vec.pop()

		if (len(self.external_data_listener_vec) == 0):
			# Nothing to process
			return

		# Make heap
		heapq.heapify(self.external_data_listener_vec) # Incorporate comparator
		while (1):
			top_edl = self.external_data_listener_vec[0]
			heapq.heappop(self.external_data_listener_vec)
			top_edl.ProcessEventsTill(self.external_data_listener_vec[0].NextEventTimestamp())
			next_event_timestamp_from_edl = top_edl.NextEventTimestamp()
			hasevents = (next_event_timestamp_from_edl != 0) and (next_event_timestamp_from_edl <= endtime)
			if (hasevents):
				heapq.heappush(self.external_data_listener_vec, top_edl)
			else:
				self.prev_external_data_listerner_vec.append(top_edl)
	
			if (len(self.external_data_listener_vec) == 1):
				self.external_data_listener_vec[0].ProcessEventsTill(endtime)
				self.prev_external_data_listerner_vec.append(self.external_data_listener_vec[0])
				self.external_data_listener_vec.pop()

			if (len(self.external_data_listener_vec) == 0):
				return

	def DeleteSources(self):
		# Check whether cleaning is required in python
		return

	def SeekHistFileSourcesTo(self, endtime):
		if (not self.first_event_enqueued):
			for it in range(0, len(self.external_data_listener_vec)):
				hasevents = self.external_data_listener_vec[it].SeekToFirstEventAfter(endtime)
				if (not hasevents):
					self.prev_external_data_listerner_vec.append(self.external_data_listener_vec[it])
					self.external_data_listener_vec.remove(it) # correct this
			self.first_event_enqueued = True
