class Request:

	def __init__(self, id, pos, hl, hlc, Vector, Td):
		#hl: hop limit
		#hlc: variabile decrementata da hl a 0
		self.id = id
		self.pos = pos
		self.hl = hl
		self.hlc = hlc
		#hl: hop limit
		#hlc: variabile decrementata da hl a 0
		self.Vtx = None
		self.Vrx = None
		self.Vector = Vector
		self.Td = Td

	def cloneReq(self):
		r=Request(self.id, self.pos, self.hl, self.hlc, self.Vector, self.Td)
		r.Vtx=self.Vtx
		r.Vrx=self.Vrx
		return r

	@staticmethod
	def dummyReq():
		return Request(1,(0,0), 8, 8, [], 0.1)

class Reply:

	def __init__(self, id, bytes):
		#hl: hop limit
		#hlc: variabile decrementata da hl a 0
		self.id = id
		self.text = bytes

	def cloneRep(self):
		return Reply(self.id, self.bytes)
