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
