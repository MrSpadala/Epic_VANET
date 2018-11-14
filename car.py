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
		self.adj = adj
	
	def modifyMsg(msg):
		#Modifico il messaggio con i miei dati
		msg.emit = self.pos
		msg.hop += 1
	
	def broadMsg(msg):
		modifyMsg(msg)
		#Se il messaggio è arrivato al limite di hop mi fermo
		if msg.hop == msg.ttl:
			return
		
		for c, i in zip(adj[plate], range(len(adj[plate])):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = Simulator.getCar(i)
				obj.infect(msg)
				
		

	def infect(msg):
		#se e' il primo messaggio faccio partire il timer di attesa
		#altrimenti aggiungo solo il messaggio alla lista
		if self.messages == []:
			messages.append(msg)
			thread.start_new_thread(timer, msg)
		else messages.append(msg)
	
	def timer(msg):
		time.sleep(2) #aspetto 3 secondi che mi arrivino altri messaggi e si riempia il buffer messages
		self.infected = True
		broadMsg(msg)
		return
