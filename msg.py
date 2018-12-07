class Msg:
	def __init__(self, numSeq, text, origin, emit, hop, ttl, emitters=None):
		#origin e' la sorgente iniziale del messaggio,
		#last_emit e' chi me lo ha mandato direttamente per ultimo
		#emitters è la lista di tutti quelli che hanno mandato questo messaggio
		self.numSeq = numSeq
		self.text = text
		self.origin = origin
		self.last_emit = emit
		self.emitters = emitters if emitters!=None else set()
		self.hop = hop
		self.ttl = ttl

	def clone(self):
		return Msg(self.numSeq, self.text, self.origin, self.last_emit, self.hop, self.ttl, self.emitters)

	@staticmethod
	def dummy():
		return Msg(1, 'ciao', (0,0), (0,0), 0, 100)
