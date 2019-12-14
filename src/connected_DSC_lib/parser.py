#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class Parser:
	def __init__(self, cars):
		self.cars	=	cars
		self.V		=	[]
		self.G		=	[]


	"""
	This algorithm is use for parse an cars object defined by car.py class.
	There was a problem because it wasn't considered if there was a car that
	not are linked with each other, therefore thare are a error named "index out of range"
	"""
	#NOT FUNCTION I THINK USE DICT 
	def CarToInputCSC(self):
		index			=	0

		for plate, car in self.cars.items():

			if plate != index:
				"""
				tmpG		=	[index] 
				tmpplate	=	index
				self.V.append(tmpplate)
				self.G.append(tmpG)
				"""
				tmpG	=	[plate] + car.neighbors
				self.V.append(plate)
				self.G.append(tmpG)
				index	+=	2
				continue

			
			index	+=	1
			tmpG	=	[plate] + car.neighbors
			self.V.append(plate)
			self.G.append(tmpG)

		return True

