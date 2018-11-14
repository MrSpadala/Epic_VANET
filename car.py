import thread
from msg import Msg

class Car:
	#Costruttore
	def __init__(self, pos):
		self.pos = pos
		self.messages = []
		self.infected = False
	
	def modifyMsg(msg):
		#Modifico il messaggio con i miei dati
		msg.emit = self.pos
		msg.hop += 1
	
	def broadMsg(msg):
		modifyMsg(msg)
		#Se il messaggio è arrivato al limite di hop mi fermo
		if msg.hop == msg.ttl:
			return
		

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
	
	def isInfected():
		return self.infected
