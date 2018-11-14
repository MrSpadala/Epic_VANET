import thread
from msg import Msg
from enum import Enum
from simulator import Simulator


class State(Enum):
	VULNERABLE = 0
	INFECTED = 1
	RECOVERED = 2
	

class Car:
	#Costruttore
	def __init__(self, plate, pos, adj):
		self.plate = plate
		self.pos = pos
		self.messages = []
		self.state = State.VULNERABLE
		self.timer_infected = None
		self.adj = adj
	
	def modifyMsg(msg):
		#Modifico il messaggio con i miei dati
		msg.emit = self.pos
		msg.hop += 1
	
	def broadMsg():
		msg = self.messages[0]
		modifyMsg(msg)
		#Se il messaggio è arrivato al limite di hop mi fermo
		if msg.hop == msg.ttl:
			return
		
		if (! evaluate_positions(self.messages, self.pos)):
			return
		#manca il controllo delle direzioni
		
		for c, i in zip(adj[plate], range(len(adj[plate]))):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = Simulator.getCar(i)
				obj.infect(msg)

		self.messages.clear()				
		

	def infect(msg):
		#se e' il primo messaggio faccio partire il timer di attesa
		#altrimenti aggiungo solo il messaggio alla lista
		if self.state == State.RECOVERED:
			return

		if self.state == State.VULNERABLE:
			self.state = State.INFECTED

		self.messages.append(msg)
		self.timer_infected = 3 / Simulator.TIME_RESOLUTION   #setta il timer infected per 3 secondi

	def evaluate_positions(messages, my_pos):   # 1 messaggio solo  ## valuta se mandare in broadcast o no
		quads = [0,0,0,0]			# flags dei quadranti: 0 quadrante inesplorato, 1 quadrante esplorato
									# abbiamo scelto quadranti divisi da una X dalla nostra posizione
		for m in messages:
			if quads[0]!=1:
				if m.emit[0]>my_pos[0] and  my_pos[1]-(abs((my_pos[0]-m.emit[0])/2)) <= m.emit[1] <= my_pos[1]-(abs((my_pos[0]-m.emit[0])/2)):		# X > myX	dx
					quads[0]=1

			if quads[1]!=1:
				if m.emit[1]>my_pos[1] and (my_pos[0]-(abs((my_pos[1]-m.emit[1])/2)) <= m.emit[0] <= my_pos[0]-(abs((my_pos[1]-m.emit[1])/2))):		# Y > myY	su
					quads[1]=1

			if quads[2]!=1:
				if m.emit[0]<my_pos[0] and (my_pos[1]-(abs((my_pos[0]-m.emit[0])/2)) <= m.emit[1] <= my_pos[1]-(abs((my_pos[0]-m.emit[0])/2))):		# X < myX	sx
					quads[2]=1

			if quads[3]!=1:
				if m.emit[1]<my_pos[1] and (my_pos[0]-(abs((my_pos[1]-m.emit[1])/2)) <= m.emit[0] <= my_pos[0]-(abs((my_pos[1]-m.emit[1])/2))):		# Y < myY	giu
					quads[3]=1
					
		print("Decidendo...")

		if quads==[1,1,1,1]:
			return False
		else:
			return True
