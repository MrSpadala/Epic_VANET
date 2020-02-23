#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
import networkx as nx

class RandomGraphGen():
	def __init__(self, nodes, m, seed=None):
		
		self.nodes	=	nodes
		self.m		=	m
		self.seed	=	seed
		self.G		=	[]
		self.V		=	[]
		self.Barabasi_Albert_Graph()
		

	def Barabasi_Albert_Graph(self):
		Graph	=	nx.barabasi_albert_graph(n=self.nodes, m=self.m, seed=self.seed)
		self.V	=	nx.nodes(Graph)
		tmpList	=	[]
		tempV	=	0
		for x in nx.edges(Graph):
			if tempV == x[0]:
				tmpList.append(x[1])
			else:

				tmpList.insert(0, tempV)
				self.G.append(tmpList)

				tmpList		=	[]
				tempV		= x[0]

		self.V	=	nx.nodes(Graph)
		
	

"""
n=100
m=int(n*0.22)	
ciao = RandomGraphGen(100,m)

grap = ciao.Barabasi_Albert_Graph()

print(ciao.G)
"""
