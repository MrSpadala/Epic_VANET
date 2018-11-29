class Msg:
	def __init__(self, numSeq, text, origin, emit, hop, ttl):
		#origin e' la sorgente iniziale del messaggio,
		#emitter e' chi me lo ha mandato direttamente
		self.numSeq = numSeq
		self.text = text
		self.origin = origin
		self.emit = emit
		self.hop = hop
		self.ttl = ttl

	@staticmethod
	def dummy():
		return Msg(1, 'ciao', (0,0), (0,0), 0, 100)
