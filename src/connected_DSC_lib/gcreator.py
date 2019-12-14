#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Gcreator:
	def __init__(self, V, G):
		self.V	=	V
		self.G	=	G
		self.R	=	[]		#list of lists
		self.U	=	None	#list


	def kindgraph():
		kind = input("Press 1 for tree, 2 for knit, 3 for path\n")
		return int(kind)

	def numnodes():
		howmany = input("How many nodes do you want?\n")
		return int(howmany)

	def knitgraph(kind, numn):
		G = []
		V = []
		total = numn+1
		for i in range(1,total):
			tmp = []
			tmp.append(i)
			if i+1 == total:
				tmp.append(1)
			else:
				tmp.append(i+1)
			G.append(tmp)
		for j in range(1,total):
			V.append(j)
		return G

	def treegraph(kindgraph, numn):
		G = []
		V = []
		total = numn+1
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
		for j in range(1,total):
			V.append(j)
		return G

	def pathgraph(kindgraph, numn):
		G = []
		V = []
		total = numn+1
		for i in range(1,total):
			print(i)
			tmp = []
			tmp.append(i)
			if i+1 != total:
				tmp.append(i+1)
			if i != 1:
				tmp.append(i-1)
			G.append(tmp)
		for j in range(1,total):
			V.append(j)
		return G
