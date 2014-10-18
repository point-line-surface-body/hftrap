import heapq

class HistoricalDispatcher() :

	first_event_enqueued = False
	'''List of external data listeners (filesources)'''
	external_data_listener_vec = []
	'''TODO: I don't think this is needed, remove it'''
	prev_external_data_listener_vec = []    
	
	def __init__(self):
		return
		
	def AddExternalDataListener(self, _new_listener_):
		self.external_data_listener_vec.append(_new_listener_)

	def RunHist(self, _endtime_):
		print('HistoricalDispatcher.RunHist')
		print('Number of ExternalDataListeners: '+str(len(self.external_data_listener_vec)))
		'''This condition is required: Some sources may have gotten empty due to 
		Seek and RunHist may be called multiple times.'''
		if (not self.first_event_enqueued):
			for edl in self.external_data_listener_vec[:]:
				hasevents = edl.ComputeEarliestDataTimestamp()
				print('hasevents: '+str(hasevents))
				if (not hasevents):
					self.prev_external_data_listener_vec.append(edl)
					self.external_data_listener_vec.remove(edl)
			self.first_event_enqueued = True
			
		if (len(self.external_data_listener_vec) == 1):
			print('No heap required')
			print('Processing till '+str(_endtime_))
			self.external_data_listener_vec[0].ProcessEventsTill(_endtime_)
			print('All events processed')
			self.prev_external_data_listener_vec.append(self.external_data_listener_vec[0])
			self.external_data_listener_vec.pop()

		if (len(self.external_data_listener_vec) == 0):
			return

		'''Add comparator'''
		heapq.heapify(self.external_data_listener_vec)

		while (1):
			top_edl = self.external_data_listener_vec[0]
			heapq.heappop(self.external_data_listener_vec)
			top_edl.ProcessEventsTill(self.external_data_listener_vec[0].NextEventTimestamp())
			next_event_timestamp_from_edl = top_edl.NextEventTimestamp()
			hasevents = (next_event_timestamp_from_edl != 0) and (next_event_timestamp_from_edl <= _endtime_)

			if (hasevents):
				heapq.heappush(self.external_data_listener_vec, top_edl)
			else:
				self.prev_external_data_listener_vec.append(top_edl)

			if (len(self.external_data_listener_vec) == 1):
				self.external_data_listener_vec[0].ProcessEventsTill(_endtime_)
				self.prev_external_data_listener_vec.append(self.external_data_listener_vec[0])
				self.external_data_listener_vec.pop()

			if (len(self.external_data_listener_vec) == 0):
				return

	def DeleteSources(self):
		return

	def SeekHistFileSourcesTo(self, _endtime_):
		'''I have removed the condition here, will it affect?'''
		for edl in self.external_data_listener_vec[:]:
			hasevents = edl.SeekToFirstEventAfter(_endtime_)
			if (not hasevents):
				self.prev_external_data_listener_vec.append(edl)
				self.external_data_listener_vec.remove(edl)