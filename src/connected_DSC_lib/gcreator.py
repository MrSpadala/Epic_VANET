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
		tmp = []
		total = numn + 1
		for i in range(1,total):
			tmp.insert(i,i)
			tmp.append(G)
			print(G)
		#print('I have {} {}'.format(kind,howmany))
		return G

	def treegraph(kindgraph, numnodes):
		G = []

		return G

	def pathgraphgraph(kindgraph, numnodes):
		G = []

		return G
