#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Parser:
	def __init__(self, cars):
		self.cars	=	cars
		self.V		=	[]
		self.S		=	[]
		self.G		=	[]

	def CarToInputCSC(self):
		index			=	0
		for plate, car in self.cars.items():
			tmpdiff		=	(plate-index)

			if tmpdiff > 0:
				for x in range(0,tmpdiff):

					tmpG		=	[index] 
					tmpplate	=	index
					#self.V.append(tmpplate)	#with this it creates deadlock
					self.G.append(tmpG)
					index += 1


				tmpG	=	[plate] + car.neighbors
				self.V.append(plate)
				self.G.append(tmpG)
				index += 1				
				continue
			
			index	+=	1
			tmpG	=	[plate] + car.neighbors
			self.V.append(plate)
			self.G.append(tmpG)

		return True
