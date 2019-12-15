#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Gcreator:
	def __init__(self, numn):
		self.V			=	[]
		self.G			=	[]
		self.numn	 	=	numn

	def knitgraph(self):
		self.G = []
		self.V = []
		G = []
		V = []
		total = self.numn#+1
		for i in range(0,total):
			tmp = []
			tmp.append(i)
			if i == 0:
				tmp.append(total-1)
			else:
				tmp.append(i-1)
			if i+1 == total:
				tmp.append(0)
			else:
				tmp.append(i+1)
			self.G.append(tmp)
		for j in range(0,total-1):
			self.V.append(j)

	def treegraph(self):
		self.G = []
		self.V = []
		G = []
		V = []
		total = self.numn+1
		x=1
		while x != total:
			y=0
			z=0
			ry=0
			tmp= []
			y=x*2
			z=y+1
			ry=x//2
			tmp.append(x)
			if x != 1:
				tmp.append(ry)
			if y < total:
				tmp.append(y)
			if z < total:	
				tmp.append(z)
			x=x+1
			G.append(tmp)
		for j in range(0,total-1):
			self.V.append(j)
		for tutti in G:
			tmp = []
			for x in tutti:

				tmp += [x-1]
			self.G.append(tmp)

	def pathgraph(self):
		self.G = []
		self.V = []
		G = []
		V = []
		total = self.numn+1
		for i in range(1,total):
			tmp = []
			tmp.append(i)
			if i+1 != total:
				tmp.append(i+1)
			if i != 1:
				tmp.append(i-1)
			G.append(tmp)
		for j in range(0,total-1):
			self.V.append(j)
		for tutti in G:
			tmp = []
			for x in tutti:
				tmp += [x-1]
			self.G.append(tmp)