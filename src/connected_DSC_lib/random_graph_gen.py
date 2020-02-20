#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx

class RandomGrapGen():
	def __init__(self, nodes, probability):
		
		self.nodes			=	nodes
		self.probability	=	probability
		

n	=	100		#nodes

p	=	0.3		#probability edge creation


	def ParseToCSCInput(self):
		'''This function is used to parse
			this random graph gen for input CSC'''


	grap = nx.fast_gnp_random_graph(n=n,p=p)

	print(nx.nodes(grap))
	print(nx.edges(grap))
