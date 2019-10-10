
class Msg:

	EMITTERS_LIMIT = 10

	def __init__(self, text, emit, hop, ttl, emitters):
		#origin e' la sorgente iniziale del messaggio,
		#last_emit e' chi me lo ha mandato direttamente per ultimo
		#emitters è la lista di tutti quelli che hanno mandato questo messaggio
		self.text = text
		self.last_emit = emit
		self.emitters = emitters
		self.hop = hop
		self.ttl = ttl

	def size(self):
		return 5+22*len(self.emitters)+len(self.text)

	def clone(self):
		return Msg(self.text, self.last_emit, self.hop, self.ttl, self.emitters)

	@staticmethod
	def dummy():
		"""Returns a dummy message, with 100 bytes of payload"""
		return Msg('\xFF'*100, (0,0), 0, 100, set())
